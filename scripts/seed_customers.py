"""
Run this once to populate your customer database with initial data.
Update this file as you onboard new customers or learn new details.

Usage: python -m scripts.seed_customers
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.database import add_customer, add_contact, get_connection


def seed():
    print("Seeding customer database...")

    add_customer(
        company_name="Sustain Commercial Solar",
        domain="sustaincommercial.co.uk",
        key_contacts=["Nick", "Dinu"],
        equipment_types=["SolarEdge", "Fox ESS"],
        site_names=[],
        open_issues=[
            "Fox ESS API sync intermittent",
        ],
        recent_promises=[],
        notes="Nick is the main point of contact. Generally responsive. Prefers concise updates.",
    )

    _add_contact_safe(
        domain="sustaincommercial.co.uk",
        name="Nick Thompson",
        email="nick@sustaincommercial.co.uk",
        role="Main point of contact",
        communication_style="Prefers concise, no-fluff updates. Responsive.",
        notes="Day-to-day operations contact. Handles most technical queries.",
    )

    _add_contact_safe(
        domain="sustaincommercial.co.uk",
        name="Dinu",
        email="dinu@sustaincommercial.co.uk",
        role="Operations",
        communication_style="",
        notes="",
    )

    add_customer(
        company_name="Bright Renewables",
        domain="brightrenewables.co.uk",
        key_contacts=["Naomi", "Samantha"],
        equipment_types=["Huawei FusionSolar"],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="Naomi handles day-to-day. Samantha is more senior.",
    )

    _add_contact_safe(
        domain="brightrenewables.co.uk",
        name="Naomi",
        email="naomi@brightrenewables.co.uk",
        role="Day-to-day contact",
        communication_style="",
        notes="Handles operational queries.",
    )

    _add_contact_safe(
        domain="brightrenewables.co.uk",
        name="Samantha",
        email="samantha@brightrenewables.co.uk",
        role="Senior contact",
        communication_style="",
        notes="More senior. Loop in for strategic or escalation items.",
    )

    add_customer(
        company_name="AMPYR",
        domain="ampyr.com",
        key_contacts=["Isla Rogers", "Peter"],
        equipment_types=["Huawei FusionSolar"],
        site_names=[],
        open_issues=[
            "Huawei FusionSolar data synchronization issues",
        ],
        recent_promises=[],
        notes="",
    )

    _add_contact_safe(
        domain="ampyr.com",
        name="Isla Rogers",
        email="isla.rogers@ampyr.com",
        role="Main contact",
        communication_style="",
        notes="",
    )

    add_customer(
        company_name="Low Carbon Energy",
        domain="lowcarbonenergy.com",
        key_contacts=[],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="Major customer. Large portfolio.",
    )

    add_customer(
        company_name="Clean Earth Energy",
        domain="cleanearthenergy.co.uk",
        key_contacts=[],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="",
    )

    add_customer(
        company_name="ROOF Energy",
        domain="roofenergy.co.uk",
        key_contacts=[],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="Part of Atrato Renewables group.",
    )

    add_customer(
        company_name="Coversol Energy",
        domain="coversol.co.uk",
        key_contacts=["Ettore"],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="Italian billing workflow. Requires XML exports for Italian invoices, multi-site invoice generation, Italian tax calculations.",
    )

    _add_contact_safe(
        domain="coversol.co.uk",
        name="Ettore",
        email="ettore@coversol.co.uk",
        role="Main contact",
        communication_style="",
        notes="Handles billing and invoicing queries.",
    )

    add_customer(
        company_name="HT Power",
        domain="htpower.co.uk",
        key_contacts=["Chiko"],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="",
    )

    _add_contact_safe(
        domain="htpower.co.uk",
        name="Chiko",
        email="chiko@htpower.co.uk",
        role="Main contact",
        communication_style="",
        notes="",
    )

    add_customer(
        company_name="Alt Group",
        domain="altgroup.co.uk",
        key_contacts=["Jordan", "Lee", "Charlotte"],
        equipment_types=["SMA"],
        site_names=["Yew Tree Farm"],
        open_issues=[],
        recent_promises=[],
        notes="Multiple contacts. Jordan, Lee, and Charlotte all involved in operations.",
    )

    _add_contact_safe(
        domain="altgroup.co.uk",
        name="Jordan",
        email="jordan@altgroup.co.uk",
        role="Operations",
        communication_style="",
        notes="",
    )

    _add_contact_safe(
        domain="altgroup.co.uk",
        name="Lee",
        email="lee@altgroup.co.uk",
        role="Operations",
        communication_style="",
        notes="",
    )

    _add_contact_safe(
        domain="altgroup.co.uk",
        name="Charlotte",
        email="charlotte@altgroup.co.uk",
        role="Operations",
        communication_style="",
        notes="",
    )

    add_customer(
        company_name="GreenHearth",
        domain="greenhearth.co.uk",
        key_contacts=[],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="",
    )

    add_customer(
        company_name="Ivegate",
        domain="ivegate.co.uk",
        key_contacts=[],
        equipment_types=[],
        site_names=[],
        open_issues=[],
        recent_promises=[],
        notes="",
    )

    print("Done. Customer database seeded with initial data.")
    print("Use 'python -m scripts.update_customer' to add issues, promises, and sites as things change.")
    print("You can re-run this script anytime - it uses INSERT OR REPLACE.")


def _add_contact_safe(domain, name, email, role="", communication_style="", notes=""):
    """Adds a contact, looking up the customer by domain first."""
    conn = get_connection()
    cursor = conn.execute("SELECT id FROM customers WHERE domain = ?", (domain,))
    row = cursor.fetchone()
    conn.close()

    if row:
        add_contact(
            customer_id=row["id"],
            name=name,
            email=email,
            role=role,
            communication_style=communication_style,
            notes=notes,
        )
    else:
        print(f"  Warning: No customer found for domain {domain}, skipping contact {name}")


if __name__ == "__main__":
    seed()
