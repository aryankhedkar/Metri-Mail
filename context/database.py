import sqlite3
import os
import json
from config import Config


def get_connection():
    """Returns a SQLite connection, creating the database if needed."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_tables(conn)
    return conn


def _ensure_tables(conn):
    """Creates tables if they do not exist."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            domain TEXT NOT NULL UNIQUE,
            key_contacts TEXT DEFAULT '[]',
            equipment_types TEXT DEFAULT '[]',
            site_names TEXT DEFAULT '[]',
            open_issues TEXT DEFAULT '[]',
            recent_promises TEXT DEFAULT '[]',
            notes TEXT DEFAULT '',
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT DEFAULT '',
            communication_style TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            contact_email TEXT NOT NULL,
            interaction_type TEXT DEFAULT 'email',
            summary TEXT DEFAULT '',
            promises_made TEXT DEFAULT '[]',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );

        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT NOT NULL UNIQUE,
            customer_id INTEGER,
            company_name TEXT DEFAULT '',
            contact_name TEXT DEFAULT '',
            contact_email TEXT NOT NULL,
            subject TEXT DEFAULT '',
            category TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            summary TEXT DEFAULT '',
            received_at TEXT DEFAULT CURRENT_TIMESTAMP,
            resolved_at TEXT,
            resolution_notes TEXT DEFAULT '',
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );
    """
    )
    conn.commit()


def get_customer_by_domain(domain):
    """Looks up a customer by their email domain."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM customers WHERE domain = ?", (domain,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return _row_to_dict(row)
    return None


def get_customer_by_email(email):
    """Looks up a customer by a contact's email address."""
    domain = email.split("@")[1].lower() if "@" in email else ""
    return get_customer_by_domain(domain)


def get_contact(email):
    """Looks up a specific contact by email."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM contacts WHERE email = ?", (email.lower(),))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def get_recent_interactions(customer_id, limit=5):
    """Gets the most recent interactions with a customer."""
    conn = get_connection()
    cursor = conn.execute(
        """SELECT * FROM interactions
           WHERE customer_id = ?
           ORDER BY created_at DESC
           LIMIT ?""",
        (customer_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_customer(company_name, domain, **kwargs):
    """Adds a new customer to the database."""
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO customers
           (company_name, domain, key_contacts, equipment_types, site_names,
            open_issues, recent_promises, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            company_name,
            domain.lower(),
            json.dumps(kwargs.get("key_contacts", [])),
            json.dumps(kwargs.get("equipment_types", [])),
            json.dumps(kwargs.get("site_names", [])),
            json.dumps(kwargs.get("open_issues", [])),
            json.dumps(kwargs.get("recent_promises", [])),
            kwargs.get("notes", ""),
        ),
    )
    conn.commit()
    conn.close()


def add_contact(customer_id, name, email, role="", communication_style="", notes=""):
    """Adds a contact to an existing customer."""
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO contacts
           (customer_id, name, email, role, communication_style, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (customer_id, name, email.lower(), role, communication_style, notes),
    )
    conn.commit()
    conn.close()


def log_interaction(customer_id, contact_email, summary, promises_made=None, interaction_type="email"):
    """Logs an interaction with a customer."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO interactions
           (customer_id, contact_email, interaction_type, summary, promises_made)
           VALUES (?, ?, ?, ?, ?)""",
        (
            customer_id,
            contact_email.lower(),
            interaction_type,
            summary,
            json.dumps(promises_made or []),
        ),
    )
    conn.commit()
    conn.close()


def update_customer_field(customer_id, field, value):
    """
    Updates a single field on a customer record.
    For JSON fields (open_issues, recent_promises, etc.), pass a list.
    """
    conn = get_connection()
    if isinstance(value, (list, dict)):
        value = json.dumps(value)
    conn.execute(
        f"UPDATE customers SET {field} = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
        (value, customer_id),
    )
    conn.commit()
    conn.close()


def log_request(email_id, contact_email, subject, category, customer_id=None,
                company_name="", contact_name="", summary=""):
    """Logs an inbound customer request for tracking."""
    conn = get_connection()
    try:
        conn.execute(
            """INSERT OR IGNORE INTO requests
               (email_id, customer_id, company_name, contact_name,
                contact_email, subject, category, summary)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (email_id, customer_id, company_name, contact_name,
             contact_email.lower(), subject, category, summary),
        )
        conn.commit()
    finally:
        conn.close()


def resolve_request(email_id, resolution_notes=""):
    """Marks a request as resolved."""
    conn = get_connection()
    conn.execute(
        """UPDATE requests
           SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP, resolution_notes = ?
           WHERE email_id = ?""",
        (resolution_notes, email_id),
    )
    conn.commit()
    conn.close()


def get_open_requests():
    """Returns all open (unresolved) requests."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM requests WHERE status = 'open' ORDER BY received_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_requests(limit=50):
    """Returns recent requests regardless of status."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM requests ORDER BY received_at DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_request_stats():
    """Returns category breakdown and resolution stats."""
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    open_count = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE status = 'open'"
    ).fetchone()[0]
    resolved_count = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE status = 'resolved'"
    ).fetchone()[0]

    category_rows = conn.execute(
        """SELECT category, COUNT(*) as count
           FROM requests GROUP BY category ORDER BY count DESC"""
    ).fetchall()
    categories = {row["category"]: row["count"] for row in category_rows}

    customer_rows = conn.execute(
        """SELECT company_name, COUNT(*) as count
           FROM requests WHERE company_name != ''
           GROUP BY company_name ORDER BY count DESC"""
    ).fetchall()
    customers = {row["company_name"]: row["count"] for row in customer_rows}

    avg_resolution = conn.execute(
        """SELECT AVG(
               (julianday(resolved_at) - julianday(received_at)) * 24
           ) as avg_hours
           FROM requests WHERE status = 'resolved'
           AND resolved_at IS NOT NULL"""
    ).fetchone()
    avg_hours = round(avg_resolution["avg_hours"], 1) if avg_resolution["avg_hours"] else None

    conn.close()

    return {
        "total": total,
        "open": open_count,
        "resolved": resolved_count,
        "avg_resolution_hours": avg_hours,
        "by_category": categories,
        "by_customer": customers,
    }


def _row_to_dict(row):
    """Converts a SQLite Row to a dict, parsing JSON fields."""
    d = dict(row)
    json_fields = [
        "key_contacts",
        "equipment_types",
        "site_names",
        "open_issues",
        "recent_promises",
    ]
    for field in json_fields:
        if field in d and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except json.JSONDecodeError:
                d[field] = []
    return d
