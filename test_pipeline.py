
from backend.db import get_db
from backend.pipeline import process_email


def main():

    db = get_db()

    # Sample incoming customer email
    sender = "thomas.mueller@example.com"

    subject = "URGENT: CNC machine stopped during production"

    body = """
    Dear Technical Support,

    Our CNC milling machine has suddenly stopped
    during production.

    The control panel displays error code E-204.

    We restarted the machine, but the problem remains.

    We cannot continue production.

    Please arrange technical support as soon as possible.

    Best regards,
    Thomas Mueller
    """

    print("\nStarting AI Email Case Assistant...\n")

    result = process_email(
        db=db,
        sender=sender,
        subject=subject,
        body=body
    )

    print("\n========== EMAIL ANALYSIS ==========")

    print("Priority:", result["analysis"]["priority"])
    print("Category:", result["analysis"]["category"])
    print("Summary:", result["analysis"]["summary"])
    print("Error codes:", result["analysis"]["error_codes"])

    print("\n========== CUSTOMER INFORMATION ==========")

    print("Customer:", result["customer"].get("company_name"))
    print("Machines found:", len(result["machines"]))
    print("Previous cases:", len(result["related_cases"]))
    print("Previous emails:", len(result["prior_emails"]))

    print("\n========== KNOWLEDGE RETRIEVAL ==========")

    for source in result["sources"][:5]:
        print(
            source["title"],
            "| Score:",
            round(source["score"], 4)
        )

    print("\n========== AI GENERATED RESPONSE ==========")

    print(result["draft"])

    print("\n========== WORKFLOW STATUS ==========")

    print("Email ID:", result["email_id"])
    print("Status:", result["status"])

    print("\nPIPELINE COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
