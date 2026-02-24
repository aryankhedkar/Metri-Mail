import json
import os
from config import Config


def load_processed():
    """Loads the set of already-processed email IDs."""
    if os.path.exists(Config.PROCESSED_EMAILS_PATH):
        with open(Config.PROCESSED_EMAILS_PATH, "r") as f:
            return set(json.load(f))
    return set()


def mark_processed(email_id):
    """Marks an email ID as processed."""
    processed = load_processed()
    processed.add(email_id)
    os.makedirs("data", exist_ok=True)
    with open(Config.PROCESSED_EMAILS_PATH, "w") as f:
        json.dump(list(processed), f)


def is_processed(email_id):
    """Checks if an email has already been processed."""
    return email_id in load_processed()
