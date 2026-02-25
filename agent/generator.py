from openai import OpenAI
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

    response = client.chat.completions.create(
        model=Config.LLM_MODEL,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

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

    return "\n".join(cleaned_lines).strip()
