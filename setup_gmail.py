"""
Run this once to authenticate with Gmail.
It will open a browser window for you to log in and grant permissions.
After this, the token is saved and you will not need to do it again.
"""
from gmail.auth import get_gmail_service


def main():
    print("Authenticating with Gmail...")
    service = get_gmail_service()

    profile = service.users().getProfile(userId="me").execute()
    print(f"Authenticated as: {profile['emailAddress']}")
    print(f"Total messages: {profile['messagesTotal']}")
    print("\nSetup complete. You can now run the agent.")


if __name__ == "__main__":
    main()
