import anthropic
from config import Config


def classify_email(email_body, subject, thread_history=None):
    """
    Uses Claude to classify an incoming email into a response type.

    Returns one of:
    - 'acknowledgment': Customer reported an issue, needs acknowledgment
    - 'technical_issue': Customer has a specific technical problem
    - 'update_request': Customer is asking for a status update
    - 'information_ask': Customer needs information or clarification
    - 'mixed_news': Situation requires delivering both good and bad news
    - 'onboarding': Related to new site setup or getting started
    - 'general': Does not fit other categories
    - 'skip': Auto-replies, out-of-office, newsletters, not requiring a response
    """
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    thread_context = ""
    if thread_history:
        recent = thread_history[-3:]
        thread_context = "\n\n".join(
            [f"From: {m['from']}\n{m['body'][:500]}" for m in recent]
        )

    response = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=50,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this customer email into exactly one category. Respond with ONLY the category name, nothing else.

Categories:
- acknowledgment: Customer reported an issue, needs a quick acknowledgment that we are on it
- technical_issue: Customer has a specific technical problem needing investigation or explanation
- update_request: Customer is asking for a status update on something in progress
- information_ask: Customer needs information, clarification, or is asking a question
- mixed_news: Situation where the response needs to deliver both good and bad news together
- options_presentation: Customer needs to choose between approaches or the situation requires presenting alternatives
- not_possible: Customer asked for something that cannot be done as requested, needs honest explanation and alternatives
- onboarding: Related to new site setup, API connections, getting started
- general: Friendly check-in, meeting coordination, or does not fit other categories
- skip: Auto-reply, out-of-office, newsletter, delivery notification, or does not need a response

Subject: {subject}

Thread context (if any):
{thread_context}

Latest email body:
{email_body[:1000]}

Category:""",
            }
        ],
    )

    category = response.content[0].text.strip().lower()

    valid_categories = [
        "acknowledgment",
        "technical_issue",
        "update_request",
        "information_ask",
        "mixed_news",
        "options_presentation",
        "not_possible",
        "onboarding",
        "general",
        "skip",
    ]

    if category in valid_categories:
        return category
    return "general"
