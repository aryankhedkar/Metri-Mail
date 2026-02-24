import base64
import re
from bs4 import BeautifulSoup
from gmail.auth import get_gmail_service
from config import Config


def get_unread_customer_emails(service=None):
    """
    Fetches unread emails from known customer domains.
    Returns a list of dicts with email metadata and content.
    """
    if service is None:
        service = get_gmail_service()

    domain_queries = " OR ".join(
        [f"from:@{domain}" for domain in Config.CUSTOMER_DOMAINS]
    )
    query = f"is:unread ({domain_queries})"

    results = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=20)
        .execute()
    )

    messages = results.get("messages", [])
    emails = []

    for msg_summary in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_summary["id"], format="full")
            .execute()
        )
        emails.append(_parse_message(msg))

    return emails


def get_thread_history(service, thread_id, max_messages=None):
    """
    Fetches the full thread for a given thread ID.
    Returns messages in chronological order.
    """
    if max_messages is None:
        max_messages = Config.MAX_THREAD_MESSAGES

    thread = (
        service.users()
        .threads()
        .get(userId="me", id=thread_id, format="full")
        .execute()
    )

    messages = thread.get("messages", [])

    if len(messages) > max_messages:
        messages = messages[-max_messages:]

    return [_parse_message(msg) for msg in messages]


def mark_as_read(service, message_id):
    """Mark a message as read by removing the UNREAD label."""
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()


def _parse_message(msg):
    """
    Extracts useful fields from a Gmail API message object.
    """
    headers = {h["name"].lower(): h["value"] for h in msg["payload"]["headers"]}

    return {
        "id": msg["id"],
        "thread_id": msg["threadId"],
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
        "body": _extract_body(msg["payload"]),
        "snippet": msg.get("snippet", ""),
    }


def _extract_body(payload):
    """
    Recursively extracts the text body from a Gmail message payload.
    Handles both simple and multipart messages.
    """
    body_text = ""

    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            body_text = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    elif payload.get("mimeType") == "text/html":
        data = payload.get("body", {}).get("data", "")
        if data:
            html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            soup = BeautifulSoup(html, "html.parser")
            body_text = soup.get_text(separator="\n", strip=True)

    elif "parts" in payload:
        plain_text = ""
        html_text = ""
        for part in payload["parts"]:
            result = _extract_body(part)
            if part.get("mimeType") == "text/plain" and result:
                plain_text = result
            elif part.get("mimeType") == "text/html" and result:
                html_text = result
            elif result:
                plain_text = plain_text or result

        body_text = plain_text or html_text

    return body_text.strip()


def extract_sender_info(from_header):
    """
    Parses the 'From' header into name and email.
    Input: 'Nick Thompson <nick@sustaincommercial.co.uk>'
    Output: {'name': 'Nick Thompson', 'email': 'nick@sustaincommercial.co.uk'}
    """
    match = re.match(r"(.+?)\s*<(.+?)>", from_header)
    if match:
        return {"name": match.group(1).strip().strip('"'), "email": match.group(2)}
    return {"name": from_header, "email": from_header}


def extract_domain(email_address):
    """Extracts domain from an email address."""
    if "@" in email_address:
        return email_address.split("@")[1].lower()
    return ""
