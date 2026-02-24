"""
Test the agent with simulated customer emails across different response types.

Usage:
    python -m scripts.test_draft                   # Run all test scenarios with Claude
    python -m scripts.test_draft --scenario 1      # Run a specific scenario
    python -m scripts.test_draft --dry-run          # Show assembled prompts without calling Claude
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.classifier import classify_email
from context.assembler import assemble_context
from context.database import get_customer_by_email, log_request
from agent.generator import generate_draft
from agent.prompt_builder import build_prompt
from gmail.reader import extract_sender_info


TEST_SCENARIOS = [
    {
        "name": "Technical Issue - Export Data Discrepancy",
        "email": {
            "id": "test_001",
            "thread_id": "thread_test_001",
            "from": "Nick Thompson <nick@sustaincommercial.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Data issue on Stells site",
            "date": "Mon, 24 Feb 2026 10:30:00 +0000",
            "body": """Hi Aryan,

Hope you're well. I've noticed the export data on the Stells site looks way off - showing about 40% higher than what we'd expect. Can you take a look when you get a chance?

Also, quick question - are we still on track for the new sites going live this week?

Cheers,
Nick""",
            "snippet": "Hi Aryan, Hope you're well...",
        },
    },
    {
        "name": "Onboarding - New Customer Setup",
        "email": {
            "id": "test_002",
            "thread_id": "thread_test_002",
            "from": "Charlotte <charlotte@altgroup.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Getting started with Metris",
            "date": "Mon, 24 Feb 2026 09:15:00 +0000",
            "body": """Hi Aryan,

We spoke with Natasha last week and we're keen to get our first batch of sites onto Metris. We have 12 sites across the Midlands, mostly SMA inverters with a couple of GoodWe systems.

What do we need from our end to get things moving? Happy to jump on a call if that's easier.

Cheers,
Charlotte""",
            "snippet": "Hi Aryan, We spoke with Natasha...",
        },
    },
    {
        "name": "Update Request - Site Connection Progress",
        "email": {
            "id": "test_003",
            "thread_id": "thread_test_003",
            "from": "Lee <lee@altgroup.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Re: Site onboarding status",
            "date": "Mon, 24 Feb 2026 14:00:00 +0000",
            "body": """Hi Aryan,

Just checking in on where we are with the site connections? I've got a board meeting Thursday and would love to show some progress.

Thanks,
Lee""",
            "snippet": "Hi Aryan, Just checking in...",
        },
    },
    {
        "name": "Not Possible - Combining Incompatible Data Sources",
        "email": {
            "id": "test_004",
            "thread_id": "thread_test_004",
            "from": "Naomi <naomi@brightrenewables.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Merging the Huawei and Hark data",
            "date": "Mon, 24 Feb 2026 11:45:00 +0000",
            "body": """Hi Aryan,

We'd like to see the Huawei generation data and the Hark meter data combined into a single site view. Is that something you can set up? We want to see generation and export on one dashboard.

Thanks,
Naomi""",
            "snippet": "Hi Aryan, We'd like to see...",
        },
    },
    {
        "name": "General - Meeting Coordination",
        "email": {
            "id": "test_005",
            "thread_id": "thread_test_005",
            "from": "Ettore <ettore@coversol.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Monthly billing call",
            "date": "Mon, 24 Feb 2026 16:00:00 +0000",
            "body": """Hi Aryan,

Shall we set up the monthly call for this week? I have a few questions about the February invoices and wanted to discuss the new site pricing as well.

Let me know what works for you.

Thanks,
Ettore""",
            "snippet": "Hi Aryan, Shall we set up...",
        },
    },
]


def run_scenario(scenario, dry_run=False, scenario_num=0):
    email = scenario["email"]
    thread = [email]

    print(f"\n{'='*70}")
    print(f"  SCENARIO {scenario_num}: {scenario['name']}")
    print(f"{'='*70}")
    print(f"  From: {email['from']}")
    print(f"  Subject: {email['subject']}")
    print(f"  Body preview: {email['body'][:120].strip()}...")

    print(f"\n  1. Classifying email...")
    if dry_run:
        email_type = _guess_type(scenario["name"])
        print(f"     Type (guessed for dry run): {email_type}")
    else:
        email_type = classify_email(email["body"], email["subject"])
        print(f"     Type: {email_type}")

    sender = extract_sender_info(email["from"])
    customer = get_customer_by_email(sender["email"])
    log_request(
        email_id=email["id"],
        contact_email=sender["email"],
        subject=email["subject"],
        category=email_type,
        customer_id=customer["id"] if customer else None,
        company_name=customer["company_name"] if customer else "",
        contact_name=sender["name"],
        summary=email.get("snippet", email["subject"]),
    )
    print(f"     Tracked: logged to request tracker")

    print(f"\n  2. Assembling context...")
    context = assemble_context(email, thread, email_type)

    if dry_run:
        system_prompt, user_message = build_prompt(context, email_type)
        print(f"\n{'─'*70}")
        print("  ASSEMBLED SYSTEM PROMPT (first 500 chars):")
        print(f"{'─'*70}")
        print(f"  {system_prompt[:500]}...")
        print(f"\n{'─'*70}")
        print("  ASSEMBLED USER MESSAGE:")
        print(f"{'─'*70}")
        print(user_message)
        print(f"{'─'*70}")
    else:
        print(f"\n  3. Generating draft with Claude...")
        draft = generate_draft(context, email_type)

        print(f"\n{'─'*70}")
        print(f"  GENERATED DRAFT ({email_type})")
        print(f"{'─'*70}")
        print(draft)
        print(f"{'─'*70}")

        if "[ARYAN:" in draft:
            print(f"\n  Placeholders that need your attention:")
            for line in draft.split("\n"):
                if "[ARYAN:" in line:
                    print(f"    > {line.strip()}")

    return email_type


def _guess_type(scenario_name):
    """Maps scenario names to expected types for dry-run mode."""
    name_lower = scenario_name.lower()
    if "technical" in name_lower:
        return "technical_issue"
    if "onboarding" in name_lower:
        return "onboarding"
    if "update" in name_lower:
        return "update_request"
    if "not possible" in name_lower:
        return "not_possible"
    if "option" in name_lower:
        return "options_presentation"
    return "general"


def main():
    parser = argparse.ArgumentParser(description="Test email agent draft generation")
    parser.add_argument(
        "--scenario",
        type=int,
        help="Run a specific scenario (1-based index)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show assembled prompts without calling Claude",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("  METRIS EMAIL AGENT - Test Suite")
    print(f"  Mode: {'DRY RUN (no API calls)' if args.dry_run else 'LIVE (calling Claude)'}")
    print(f"  Scenarios: {len(TEST_SCENARIOS)} available")
    print("=" * 70)

    if args.scenario:
        idx = args.scenario - 1
        if 0 <= idx < len(TEST_SCENARIOS):
            run_scenario(TEST_SCENARIOS[idx], dry_run=args.dry_run, scenario_num=args.scenario)
        else:
            print(f"  Invalid scenario number. Choose 1-{len(TEST_SCENARIOS)}.")
            return
    else:
        for i, scenario in enumerate(TEST_SCENARIOS, 1):
            run_scenario(scenario, dry_run=args.dry_run, scenario_num=i)

    print(f"\n{'='*70}")
    print("  Done.")
    print("=" * 70)


if __name__ == "__main__":
    main()
