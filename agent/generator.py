import anthropic
from config import Config
from agent.prompt_builder import build_prompt


def generate_draft(assembled_context, email_type):
    """
    Calls Claude API to generate an email draft.

    Args:
        assembled_context: The full context string from assembler.py
        email_type: Classification string

    Returns:
        The generated email draft as a string
    """
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    system_prompt, user_message = build_prompt(assembled_context, email_type)

    response = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    draft = response.content[0].text.strip()

    draft = _clean_draft(draft)

    return draft


def _clean_draft(draft):
    """
    Removes any unwanted formatting from the generated draft.
    Claude sometimes wraps emails in markdown code blocks or adds headers.
    """
    if draft.startswith("```"):
        lines = draft.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        draft = "\n".join(lines)

    lines = draft.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.strip().lower().startswith("subject:"):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()
