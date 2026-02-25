"""
Three realistic customer scenarios for Maria's review.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.classifier import classify_email
from context.assembler import assemble_context
from context.database import get_customer_by_email
from agent.generator import generate_draft
from gmail.reader import extract_sender_info


DEMO_SCENARIOS = [
    {
        "name": "Isla from AMPYR - inverter offline for 3 days, wants an explanation",
        "email": {
            "id": "demo_001",
            "thread_id": "thread_demo_001",
            "from": "Isla Rogers <isla.rogers@ampyr.com>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "Inverter offline at Warrington site",
            "date": "Mon, 24 Feb 2026 09:12:00 +0000",
            "body": """Hi Aryan,

One of our Huawei inverters at the Warrington site has been showing as offline since Friday. We've had no generation data coming through and I'm getting questions from the asset owner about lost revenue.

Can you look into what's going on and let me know if this is something on the Metris side or if we need to get someone out to site?

Thanks,
Isla""",
            "snippet": "Inverter offline since Friday at Warrington...",
        },
    },
    {
        "name": "Nick from Sustain - February report looks wrong, needs it for investors",
        "email": {
            "id": "demo_002",
            "thread_id": "thread_demo_002",
            "from": "Nick Thompson <nick@sustaincommercial.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "February performance report - numbers don't add up",
            "date": "Mon, 24 Feb 2026 11:45:00 +0000",
            "body": """Hi Aryan,

I've pulled the February performance report for the portfolio and a few things look off. The self-consumption figures for three of the Fox ESS sites are showing as negative, which obviously can't be right. The export numbers also seem inflated on those same sites.

I need to send the investor report out by Thursday so would appreciate a quick turnaround on this. Can you check what's going on with the data?

Cheers,
Nick""",
            "snippet": "February report has negative self-consumption on Fox ESS sites...",
        },
    },
    {
        "name": "Ettore from Coversol - invoices generated with wrong tariff rate",
        "email": {
            "id": "demo_003",
            "thread_id": "thread_demo_003",
            "from": "Ettore <ettore@coversol.co.uk>",
            "to": "aryan@metrisenergy.com",
            "cc": "",
            "subject": "January invoices - tariff rate issue",
            "date": "Mon, 24 Feb 2026 14:30:00 +0000",
            "body": """Hi Aryan,

I've been reviewing the January invoices that were generated and noticed that three sites are still using the old tariff rate (14.2p/kWh) instead of the new rate we agreed on (15.8p/kWh) from January 1st. The sites affected are Basildon, Chelmsford, and Southend.

Can these be regenerated with the correct rate? I need to get the XML exports out to our Italian office by end of week.

Thanks,
Ettore""",
            "snippet": "January invoices using old tariff rate instead of new 15.8p/kWh...",
        },
    },
]


def run_demo():
    print()
    print("=" * 70)
    print("  MetriMail Demo - Three Real Scenarios")
    print("=" * 70)

    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        email = scenario["email"]
        thread = [email]

        print(f"\n\n{'=' * 70}")
        print(f"  SCENARIO {i}: {scenario['name']}")
        print(f"{'=' * 70}")
        print(f"  From: {email['from']}")
        print(f"  Subject: {email['subject']}")
        print()
        print(f"  INBOUND EMAIL:")
        print(f"  {'─' * 60}")
        for line in email["body"].strip().split("\n"):
            print(f"  {line}")
        print(f"  {'─' * 60}")

        print(f"\n  Classifying...")
        email_type = classify_email(email["body"], email["subject"])
        print(f"  → Classified as: {email_type}")

        print(f"  Assembling context...")
        context = assemble_context(email, thread, email_type)

        print(f"  Generating draft...")
        draft = generate_draft(context, email_type)

        print(f"\n  {'━' * 60}")
        print(f"  METRIMAIL DRAFT → (type: {email_type})")
        print(f"  {'━' * 60}")
        print()
        for line in draft.split("\n"):
            print(f"  {line}")
        print()
        print(f"  {'━' * 60}")

        if "[ARYAN:" in draft:
            print(f"\n  ⚠ Placeholders for Aryan to fill in:")
            for line in draft.split("\n"):
                if "[ARYAN:" in line:
                    print(f"    → {line.strip()}")

    print(f"\n\n{'=' * 70}")
    print("  Done.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
