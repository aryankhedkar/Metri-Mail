import json
from context.database import (
    get_customer_by_email,
    get_contact,
    get_recent_interactions,
)
from gmail.reader import extract_sender_info, extract_domain


def assemble_context(email, thread_history, email_type):
    """
    Builds a complete context packet for the Claude API call.

    Args:
        email: Dict with 'from', 'subject', 'body', etc.
        thread_history: List of message dicts from the thread
        email_type: Classification string from classifier

    Returns:
        A formatted string containing all context Claude needs.
    """
    sender = extract_sender_info(email["from"])
    domain = extract_domain(sender["email"])

    customer = get_customer_by_email(sender["email"])
    contact = get_contact(sender["email"])

    sections = []

    sections.append(_build_sender_section(sender, contact, customer))

    sections.append(f"EMAIL TYPE: {email_type}")

    if customer:
        sections.append(_build_customer_section(customer))

    if customer:
        interactions = get_recent_interactions(customer["id"], limit=5)
        if interactions:
            sections.append(_build_interaction_section(interactions))

    if len(thread_history) > 1:
        sections.append(_build_thread_section(thread_history))

    sections.append(_build_email_section(email))

    return "\n\n---\n\n".join(sections)


def _build_sender_section(sender, contact, customer):
    """Who sent this email and what do we know about them."""
    lines = [f"SENDER: {sender['name']} <{sender['email']}>"]

    if customer:
        lines.append(f"COMPANY: {customer['company_name']}")

    if contact:
        if contact.get("role"):
            lines.append(f"ROLE: {contact['role']}")
        if contact.get("communication_style"):
            lines.append(f"COMMUNICATION STYLE: {contact['communication_style']}")
        if contact.get("notes"):
            lines.append(f"CONTACT NOTES: {contact['notes']}")

    return "\n".join(lines)


def _build_customer_section(customer):
    """What we know about this customer's account."""
    lines = ["CUSTOMER CONTEXT:"]

    if customer.get("equipment_types"):
        lines.append(f"  Equipment: {', '.join(customer['equipment_types'])}")

    if customer.get("site_names"):
        lines.append(f"  Sites: {', '.join(customer['site_names'])}")

    if customer.get("open_issues"):
        lines.append("  Open issues:")
        for issue in customer["open_issues"]:
            lines.append(f"    - {issue}")

    if customer.get("recent_promises"):
        lines.append("  Promises made (IMPORTANT - reference these if relevant):")
        for promise in customer["recent_promises"]:
            lines.append(f"    - {promise}")

    if customer.get("notes"):
        lines.append(f"  Notes: {customer['notes']}")

    return "\n".join(lines)


def _build_interaction_section(interactions):
    """Recent interaction history."""
    lines = ["RECENT INTERACTIONS:"]
    for interaction in interactions:
        lines.append(
            f"  [{interaction['created_at']}] {interaction['interaction_type']}: {interaction['summary']}"
        )
        promises = interaction.get("promises_made", "[]")
        if isinstance(promises, str):
            try:
                promises = json.loads(promises)
            except json.JSONDecodeError:
                promises = []
        if promises:
            for promise in promises:
                lines.append(f"    Promise: {promise}")

    return "\n".join(lines)


def _build_thread_section(thread_history):
    """The email thread leading up to this message."""
    lines = ["THREAD HISTORY (oldest to newest):"]

    for msg in thread_history[:-1]:
        lines.append(f"\n  From: {msg['from']}")
        lines.append(f"  Date: {msg['date']}")
        body = msg["body"][:800]
        if len(msg["body"]) > 800:
            body += "\n  [... truncated]"
        lines.append(f"  Body:\n  {body}")

    return "\n".join(lines)


def _build_email_section(email):
    """The actual email we need to respond to."""
    return f"""EMAIL TO RESPOND TO:
From: {email['from']}
Subject: {email['subject']}
Date: {email['date']}

{email['body']}"""
