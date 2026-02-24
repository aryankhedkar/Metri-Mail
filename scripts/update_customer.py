"""
Quick CLI for updating customer context.

Usage:
    python -m scripts.update_customer "Sustain Commercial Solar" --add-issue "SolarEdge API returning 403 since Monday"
    python -m scripts.update_customer "Sustain Commercial Solar" --add-promise "Will resolve SolarEdge issue by Friday"
    python -m scripts.update_customer "Sustain Commercial Solar" --remove-issue "Fox ESS API sync intermittent"
    python -m scripts.update_customer "Sustain Commercial Solar" --add-site "Stells Farm"
    python -m scripts.update_customer "Sustain Commercial Solar" --notes "Nick prefers quick updates, no fluff"
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.database import get_connection, update_customer_field


def main():
    parser = argparse.ArgumentParser(description="Update customer context")
    parser.add_argument("company", help="Company name (partial match)")
    parser.add_argument("--add-issue", help="Add an open issue")
    parser.add_argument("--remove-issue", help="Remove a resolved issue")
    parser.add_argument("--add-promise", help="Add a promise made")
    parser.add_argument("--remove-promise", help="Remove a fulfilled promise")
    parser.add_argument("--add-site", help="Add a site name")
    parser.add_argument("--notes", help="Update notes (appends)")
    args = parser.parse_args()

    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM customers WHERE company_name LIKE ?",
        (f"%{args.company}%",),
    )
    row = cursor.fetchone()

    if not row:
        print(f"No customer found matching '{args.company}'")
        conn.close()
        return

    customer = dict(row)
    customer_id = customer["id"]
    print(f"Updating: {customer['company_name']}")

    if args.add_issue:
        issues = json.loads(customer.get("open_issues", "[]"))
        issues.append(args.add_issue)
        update_customer_field(customer_id, "open_issues", issues)
        print(f"  Added issue: {args.add_issue}")

    if args.remove_issue:
        issues = json.loads(customer.get("open_issues", "[]"))
        issues = [i for i in issues if args.remove_issue.lower() not in i.lower()]
        update_customer_field(customer_id, "open_issues", issues)
        print(f"  Removed issue matching: {args.remove_issue}")

    if args.add_promise:
        promises = json.loads(customer.get("recent_promises", "[]"))
        promises.append(args.add_promise)
        update_customer_field(customer_id, "recent_promises", promises)
        print(f"  Added promise: {args.add_promise}")

    if args.remove_promise:
        promises = json.loads(customer.get("recent_promises", "[]"))
        promises = [p for p in promises if args.remove_promise.lower() not in p.lower()]
        update_customer_field(customer_id, "recent_promises", promises)
        print(f"  Removed promise matching: {args.remove_promise}")

    if args.add_site:
        sites = json.loads(customer.get("site_names", "[]"))
        sites.append(args.add_site)
        update_customer_field(customer_id, "site_names", sites)
        print(f"  Added site: {args.add_site}")

    if args.notes:
        existing = customer.get("notes", "")
        updated = f"{existing}\n{args.notes}" if existing else args.notes
        update_customer_field(customer_id, "notes", updated)
        print(f"  Updated notes")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
