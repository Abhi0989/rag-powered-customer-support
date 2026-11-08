
from email.utils import parseaddr

from backend.db import get_db
from backend.gmail_client import fetch_unread_emails
from backend.pipeline import process_email


def main():
    print("\nConnecting to MongoDB...")
    db = get_db()

    print("\nFetching unread Gmail messages...")
    emails = fetch_unread_emails(max_results=10)

    print("Unread emails retrieved:", len(emails))

    processed_count = 0
    skipped_count = 0

    for email in emails:

        sender_name, sender_address = parseaddr(email["sender"])
        sender_address = sender_address.strip().lower()

        message_id = email["gmail_message_id"]

        subject = email.get("subject", "")
        body = email.get("body", "")

        print("\n===================================")
        print("Checking email:", subject)
        print("Sender:", sender_address)

        # Ignore emails without a valid sender.
        if not sender_address:
            print("Skipped: Invalid sender address.")
            skipped_count += 1
            continue

        # Check whether this Gmail message was already processed.
        existing_email = db.emails.find_one({
            "gmail_message_id": message_id
        })

        if existing_email:
            print("Skipped: This email was already processed.")
            skipped_count += 1
            continue

        # Only process emails from registered customers.
        customer = db.customers.find_one({
            "$or": [
                {"email": sender_address},
                {"additional_emails": sender_address}
            ]
        })

        if not customer:
            print("Skipped: Sender is not a registered customer.")
            skipped_count += 1
            continue

        # Ignore messages without meaningful content.
        if not subject.strip() or not body.strip():
            print("Skipped: Email has no subject or body.")
            skipped_count += 1
            continue

        print("\nCustomer found:", customer.get("company_name"))

        print("\nStarting AI email processing...")

        result = process_email(
            db=db,
            sender=email["sender"],
            subject=subject,
            body=body,
            gmail_message_id=message_id
        )

        print("\n========== PROCESSING RESULT ==========")

        print("Customer:", result["customer"].get("company_name"))
        print("Customer history found:", result["customer_found"])

        print("Priority:", result["analysis"]["priority"])
        print("Category:", result["analysis"]["category"])
        print("Summary:", result["analysis"]["summary"])
        print("Error codes:", result["analysis"]["error_codes"])

        print("\nMachines found:", len(result["machines"]))
        print("Previous cases:", len(result["related_cases"]))
        print("Previous emails:", len(result["prior_emails"]))

        print("\nAI SUGGESTED RESPONSE:")
        print("-----------------------------------")
        print(result["draft"])
        print("-----------------------------------")

        print("\nWorkflow status:", result["status"])
        print("Saved email ID:", result["email_id"])

        processed_count += 1

    print("\n===================================")
    print("GMAIL PIPELINE TEST COMPLETED")
    print("Processed:", processed_count)
    print("Skipped:", skipped_count)


if __name__ == "__main__":
    main()
