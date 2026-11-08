
import os
import base64

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Read-only access for the initial Gmail integration.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Project root directory.
BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_gmail_service():
    """
    Authenticate with Google and return Gmail API service.
    """

    credentials = None

    # Load previously saved authentication.
    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    # Refresh expired credentials or request new authorization.
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:

        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(
                "credentials.json not found in the project root."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0,
            open_browser=True
        )

        # Save authentication for future runs.
        TOKEN_FILE.write_text(credentials.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service


def decode_email_body(payload):
    """
    Extract plain-text email content from Gmail MIME payload.
    """

    if "parts" in payload:

        for part in payload["parts"]:

            result = decode_email_body(part)

            if result:
                return result

    body_data = payload.get("body", {}).get("data")

    if body_data:

        decoded_bytes = base64.urlsafe_b64decode(
            body_data
        )

        return decoded_bytes.decode(
            "utf-8",
            errors="replace"
        )

    return ""


def get_email_details(service, message_id):
    """
    Retrieve sender, subject and body of one Gmail message.
    """

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = message.get(
        "payload", {}
    ).get("headers", [])

    email_headers = {
        header["name"].lower(): header["value"]
        for header in headers
    }

    sender = email_headers.get("from", "")
    subject = email_headers.get("subject", "")

    body = decode_email_body(
        message.get("payload", {})
    )

    return {
        "gmail_message_id": message_id,
        "thread_id": message.get("threadId"),
        "sender": sender,
        "subject": subject,
        "body": body,
        "received_at": message.get("internalDate")
    }


def fetch_unread_emails(max_results=5):
    """
    Retrieve unread emails from the Gmail inbox.
    Does not mark emails as read or modify them.
    """

    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])

    email_list = []

    for message in messages:

        email_details = get_email_details(
            service,
            message["id"]
        )

        email_list.append(email_details)

    return email_list
