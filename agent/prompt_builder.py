import os
from config import Config


def build_prompt(assembled_context, email_type):
    """
    Constructs the full prompt for the Claude API call.

    Returns a tuple: (system_prompt, user_message)
    """
    system_prompt = _load_prompt_file(Config.SYSTEM_PROMPT_PATH)

    type_instructions = _load_type_instructions(email_type)

    full_system_prompt = f"{system_prompt}\n\n---\n\n## RESPONSE TYPE INSTRUCTIONS\n\n{type_instructions}"

    user_message = f"""Here is the context and the email you need to respond to. Draft a reply following the guidelines and the "{email_type}" response type instructions.

{assembled_context}

---

Write the email draft now. Critical reminders:
- Start with "Hi [First Name]," on its own line
- Follow the email arc for this response type: warm open > good news/status > blockers/asks > momentum close
- Do NOT use contractions: "I will" not "I'll", "do not" not "don't", "it is" not "it's"
- Do NOT use banned openings: "Hope you are well", "I wanted to reach out", "Just following up"
- Do NOT use banned closings: "Please do not hesitate to reach out", "Let me know if you have any questions"
- Flag anything you are unsure about with [ARYAN: ...]
- End with a forward-looking line BEFORE "Best,\\nAryan" (e.g., "Looking forward to it." or "I will keep you posted.")
- End with "Best,\\nAryan" on its own line"""

    return full_system_prompt, user_message


def _load_prompt_file(path):
    """Loads a prompt file from disk."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def _load_type_instructions(email_type):
    """Loads the type-specific instructions."""
    path = os.path.join("prompts", "email_types", f"{email_type}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    fallback_path = os.path.join("prompts", "email_types", "general.md")
    if os.path.exists(fallback_path):
        with open(fallback_path, "r", encoding="utf-8") as f:
            return f.read()

    return "RESPONSE TYPE: GENERAL\nFollow the standard email guidelines."
