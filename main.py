"""
Metris Email Agent
==================
Watches Gmail for customer emails, generates draft responses using Claude,
and saves them to your drafts folder for review.

Usage:
    python main.py              # Run once (process current unread emails)
    python main.py --watch      # Run continuously, checking every N seconds
    python main.py --test       # Dry run: show what would be drafted without saving
"""

import sys
import time
import argparse
from datetime import datetime

from gmail.auth import get_gmail_service
from gmail.reader import get_unread_customer_emails, get_thread_history, extract_sender_info, mark_as_read
from gmail.drafter import create_draft_reply
from context.classifier import classify_email
from context.assembler import assemble_context
from context.tracker import is_processed, mark_processed
from context.database import get_customer_by_email, log_request
from agent.generator import generate_draft
from config import Config


SKIP_DOMAINS = {
    "metrisenergy.com",
    "calendar.google.com",
    "google.com",
    "slack.com",
    "notifications.slack.com",
    "noreply",
    "no-reply",
    "mailer-daemon",
    "postmaster",
    "cursor.com",
    "github.com",
    "linear.app",
    "vercel.com",
    "stripe.com",
}

SKIP_SUBJECT_PATTERNS = [
    "invitation:",
    "accepted:",
    "declined:",
    "updated invitation:",
    "canceled event:",
    "out of office",
    "automatic reply",
    "auto-reply",
    "undeliverable",
    "delivery status",
    "read receipt",
]


def _should_skip(sender_email, subject):
    sender_lower = sender_email.lower()
    domain = sender_lower.split("@")[1] if "@" in sender_lower else ""
    local = sender_lower.split("@")[0] if "@" in sender_lower else sender_lower

    if domain in SKIP_DOMAINS:
        return True
    if local in ("noreply", "no-reply", "mailer-daemon", "postmaster"):
        return True

    subject_lower = subject.lower()
    for pattern in SKIP_SUBJECT_PATTERNS:
        if pattern in subject_lower:
            return True

    return False


def process_emails(dry_run=False):
    """
    Main processing function. Fetches unread customer emails,
    generates drafts, and saves them to Gmail.
    """
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for customer emails...")

    service = get_gmail_service()
    emails = get_unread_customer_emails(service)

    if not emails:
        print("  No unread customer emails found.")
        return 0

    print(f"  Found {len(emails)} unread customer email(s).")
    drafts_created = 0

    for email in emails:
        if is_processed(email["id"]):
            print(f"  Skipping (already processed): {email['subject']}")
            continue

        sender = extract_sender_info(email["from"])

        if _should_skip(sender["email"], email["subject"]):
            print(f"  Skipping (filtered): {email['subject']}")
            mark_processed(email["id"])
            continue

        print(f"\n  Processing: {email['subject']}")
        print(f"  From: {sender['name']} <{sender['email']}>")

        print("  Fetching thread history...")
        thread_history = get_thread_history(service, email["thread_id"])

        print("  Classifying email type...")
        email_type = classify_email(
            email["body"], email["subject"], thread_history
        )
        print(f"  Type: {email_type}")

        if email_type == "skip":
            print("  Skipping (auto-reply/newsletter/no response needed).")
            mark_processed(email["id"])
            continue

        customer = get_customer_by_email(sender["email"])
        log_request(
            email_id=email["id"],
            contact_email=sender["email"],
            subject=email["subject"],
            category=email_type,
            customer_id=customer["id"] if customer else None,
            company_name=customer["company_name"] if customer else "",
            contact_name=sender["name"],
            summary=email["snippet"] if email.get("snippet") else email["subject"],
        )
        print(f"  Logged request: {email_type} from {sender['name']}")

        print("  Assembling context...")
        context = assemble_context(email, thread_history, email_type)

        print("  Generating draft with Claude...")
        draft_body = generate_draft(context, email_type)

        if dry_run:
            print(f"\n{'='*60}")
            print(f"DRAFT (dry run - not saved)")
            print(f"{'='*60}")
            print(f"To: {email['from']}")
            print(f"Subject: Re: {email['subject']}")
            print(f"Type: {email_type}")
            print(f"{'='*60}")
            print(draft_body)
            print(f"{'='*60}\n")
        else:
            print("  Saving draft to Gmail...")
            draft = create_draft_reply(service, email, draft_body)
            print(f"  Draft created (ID: {draft['id']})")

        mark_processed(email["id"])
        drafts_created += 1

    print(f"\n  Done. Created {drafts_created} draft(s).")
    return drafts_created


def watch_mode():
    """Runs the agent continuously, checking at intervals."""
    interval = Config.CHECK_INTERVAL_SECONDS
    print(f"Starting watch mode. Checking every {interval} seconds.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            process_emails()
            print(f"\nNext check in {interval} seconds...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="Metris Email Agent")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run continuously, checking for new emails at intervals",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Dry run: show drafts without saving to Gmail",
    )
    args = parser.parse_args()

    import os
    os.makedirs("data", exist_ok=True)

    if args.watch:
        watch_mode()
    else:
        process_emails(dry_run=args.test)


if __name__ == "__main__":
    main()
