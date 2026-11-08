
from dotenv import load_dotenv
from backend.db import get_db
from backend.case_retrieval import get_customer_context

load_dotenv()

db = get_db()

# Test using the fictional Innovac customer
sender_email = "thomas.mueller@example.com"

context = get_customer_context(
    db,
    sender_email
)

if not context.get("customer_found", True):

    print(context["message"])

else:

    print("\nCUSTOMER:")
    print(context["customer"]["company_name"])

    print("\nMACHINES:")
    for machine in context["machines"]:
        print(
            machine["machine_name"],
            machine["model"]
        )

    print("\nTECHNICAL CASES:")
    for case in context["cases"]:
        print(
            case["case_number"],
            case["subject"],
            case["status"]
        )

    print("\nWARRANTIES:")
    for warranty in context["warranties"]:
        print(
            warranty["warranty_type"],
            warranty["status"]
        )

    print("\nSERVICE RECORDS:")
    for record in context["service_records"]:
        print(record["work_performed"])

    print("\nTECHNICAL DOCUMENTS:")
    for document in context["knowledge_documents"]:
        print(document["title"])

    print("\nRETRIEVAL COMPLETED SUCCESSFULLY!")
