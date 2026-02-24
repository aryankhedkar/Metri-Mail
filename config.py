import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Gmail
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")

    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250514")

    # Agent
    MAX_THREAD_MESSAGES = int(os.getenv("MAX_THREAD_MESSAGES", "10"))
    CUSTOMER_DOMAINS = [
        d.strip()
        for d in os.getenv("CUSTOMER_DOMAINS", "").split(",")
        if d.strip()
    ]
    CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))
    MY_EMAIL = os.getenv("MY_EMAIL", "")

    # Paths
    DATABASE_PATH = os.path.join("data", "customers.db")
    PROCESSED_EMAILS_PATH = os.path.join("data", "processed_emails.json")
    SYSTEM_PROMPT_PATH = os.path.join("prompts", "system_prompt.md")
