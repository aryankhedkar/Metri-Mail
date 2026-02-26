import time
from openai import OpenAI, RateLimitError
from config import Config
from agent.prompt_builder import build_prompt


def generate_draft(assembled_context, email_type):
    """
    Calls OpenAI API to generate an email draft.

    Args:
        assembled_context: The full context string from assembler.py
        email_type: Classification string

    Returns:
        The generated email draft as a string
    """
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    system_prompt, user_message = build_prompt(assembled_context, email_type)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=Config.LLM_MODEL,
                max_completion_tokens=1500,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            break
        except RateLimitError as e:
            if attempt == 2:
                raise
            wait = 60 * (attempt + 1)
            print(f"  Rate limit hit, waiting {wait}s before retry...")
            time.sleep(wait)

    draft = response.choices[0].message.content.strip()

    draft = _clean_draft(draft)

    return draft


def _clean_draft(draft):
    """
    Removes any unwanted formatting from the generated draft.
    LLMs sometimes wrap emails in markdown code blocks or add headers.
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

    draft = "\n".join(cleaned_lines).strip()

    import re
    draft = re.sub(r"\*\*(.+?)\*\*", r"\1", draft)
    draft = re.sub(r"(?<!\s)\*(.+?)\*(?!\s)", r"\1", draft)
    draft = re.sub(r"^#{1,6}\s+", "", draft, flags=re.MULTILINE)
    draft = draft.replace("\u2014", ", ")
    draft = draft.replace("\u2013", "-")

    return draft
