
from backend.gmail_client import fetch_unread_emails


print("\nConnecting to Gmail...\n")

emails = fetch_unread_emails(max_results=5)

print("Unread emails found:", len(emails))

for index, email in enumerate(emails, start=1):

    print("\n========== EMAIL", index, "==========")

    print("Sender:", email["sender"])
    print("Subject:", email["subject"])
    print("Body:", email["body"][:1000])

print("\nGMAIL INTEGRATION TEST COMPLETED!")
