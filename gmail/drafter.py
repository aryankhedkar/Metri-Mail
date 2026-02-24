import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from gmail.auth import get_gmail_service


def create_draft_reply(service, original_message, draft_body, cc=None):
    """
    Creates a draft reply to an existing email.

    Args:
        service: Gmail API service object
        original_message: Dict from reader.py with 'id', 'thread_id', 'from', 'subject', etc.
        draft_body: The email body text to use in the draft
        cc: Optional CC addresses (string, comma-separated)

    Returns:
        The created draft object from Gmail API
    """
    message = MIMEMultipart("alternative")
    message["to"] = original_message["from"]
    message["subject"] = _build_reply_subject(original_message["subject"])
    message["In-Reply-To"] = original_message["id"]
    message["References"] = original_message["id"]

    if cc:
        message["cc"] = cc

    text_part = MIMEText(draft_body, "plain")
    message.attach(text_part)

    html_body = _text_to_html(draft_body)
    html_part = MIMEText(html_body, "html")
    message.attach(html_part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body={
                "message": {
                    "raw": raw,
                    "threadId": original_message["thread_id"],
                }
            },
        )
        .execute()
    )

    return draft


def _build_reply_subject(subject):
    """Ensures subject starts with 'Re:' without double-prefixing."""
    if subject.lower().startswith("re:"):
        return subject
    return f"Re: {subject}"


def _text_to_html(text):
    """
    Converts plain text to simple HTML for email.
    Preserves paragraph breaks and basic structure.
    """
    paragraphs = text.split("\n\n")
    html_parts = []

    for para in paragraphs:
        lines = para.split("\n")
        processed_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                if not in_list:
                    processed_lines.append("<ul>")
                    in_list = True
                item_text = stripped[2:]
                processed_lines.append(f"  <li>{item_text}</li>")
            else:
                if in_list:
                    processed_lines.append("</ul>")
                    in_list = False
                if stripped:
                    processed_lines.append(f"<p>{stripped}</p>")

        if in_list:
            processed_lines.append("</ul>")

        html_parts.extend(processed_lines)

    body_html = "\n".join(html_parts)

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333; line-height: 1.5;">
    {body_html}
    </body>
    </html>
    """
