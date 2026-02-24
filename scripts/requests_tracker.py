"""
View and manage tracked customer requests.

Usage:
    python -m scripts.requests_tracker                     # Show dashboard summary
    python -m scripts.requests_tracker --open              # List open requests
    python -m scripts.requests_tracker --all               # List all recent requests
    python -m scripts.requests_tracker --resolve EMAIL_ID  # Mark a request as resolved
    python -m scripts.requests_tracker --resolve EMAIL_ID --notes "Fixed the API issue"
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.database import (
    get_open_requests,
    get_all_requests,
    get_request_stats,
    resolve_request,
)


def show_dashboard():
    stats = get_request_stats()

    if stats["total"] == 0:
        print("\n  No requests tracked yet.")
        print("  Requests are logged automatically when MetriMail processes emails.")
        print("  Run 'python main.py' or 'python -m scripts.test_draft' to start tracking.\n")
        return

    print(f"\n{'='*60}")
    print("  METRIMAIL - Request Tracker")
    print(f"{'='*60}")

    print(f"\n  Total requests:    {stats['total']}")
    print(f"  Open:              {stats['open']}")
    print(f"  Resolved:          {stats['resolved']}")
    if stats["avg_resolution_hours"] is not None:
        print(f"  Avg resolution:    {stats['avg_resolution_hours']}h")

    if stats["by_category"]:
        print(f"\n  {'─'*40}")
        print("  BY CATEGORY:")
        for category, count in stats["by_category"].items():
            bar = "█" * min(count, 30)
            print(f"    {category:<22} {count:>3}  {bar}")

    if stats["by_customer"]:
        print(f"\n  {'─'*40}")
        print("  BY CUSTOMER:")
        for customer, count in stats["by_customer"].items():
            bar = "█" * min(count, 30)
            print(f"    {customer:<22} {count:>3}  {bar}")

    print(f"\n{'='*60}\n")


def show_requests(requests, label):
    if not requests:
        print(f"\n  No {label} requests.\n")
        return

    print(f"\n{'='*60}")
    print(f"  {label.upper()} REQUESTS ({len(requests)})")
    print(f"{'='*60}")

    for r in requests:
        status_marker = "●" if r["status"] == "open" else "○"
        print(f"\n  {status_marker} [{r['category']}] {r['subject']}")
        print(f"    From: {r['contact_name']} ({r['company_name'] or 'unknown'})")
        print(f"    Received: {r['received_at']}")
        if r["status"] == "resolved" and r["resolved_at"]:
            print(f"    Resolved: {r['resolved_at']}")
        if r["resolution_notes"]:
            print(f"    Notes: {r['resolution_notes']}")
        print(f"    ID: {r['email_id']}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="MetriMail Request Tracker")
    parser.add_argument("--open", action="store_true", help="Show open requests")
    parser.add_argument("--all", action="store_true", help="Show all recent requests")
    parser.add_argument("--resolve", metavar="EMAIL_ID", help="Mark a request as resolved")
    parser.add_argument("--notes", default="", help="Resolution notes (used with --resolve)")
    args = parser.parse_args()

    if args.resolve:
        resolve_request(args.resolve, args.notes)
        print(f"  Resolved: {args.resolve}")
        if args.notes:
            print(f"  Notes: {args.notes}")
        return

    if args.open:
        show_requests(get_open_requests(), "open")
    elif args.all:
        show_requests(get_all_requests(), "all")
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
