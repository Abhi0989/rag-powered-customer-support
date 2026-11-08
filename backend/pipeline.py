
import uuid
import json

from datetime import datetime, timezone
from email.utils import parseaddr

from backend.ai import analyze_email, generate_draft
from backend.retrieval import retrieve_similar_chunks
from backend.case_retrieval import get_customer_context


def process_email(
    db,
    sender,
    subject,
    body,
    gmail_message_id=None
):
    # Extract the actual email address from:
    # Thomas Mueller <thomas@example.com>
    sender_name, sender_email = parseaddr(sender)

    sender = sender_email.strip().lower()

    if not sender:
        raise ValueError("Could not identify the sender email address.")

    print("\nStep 1: Analyzing incoming email...")

    analysis = analyze_email(subject, body)

    print("\nStep 2: Retrieving customer history...")

    context = get_customer_context(db, sender)

    customer_found = context.get("customer_found", False)

    # Find the original MongoDB customer document.
    # Support both primary and additional email addresses.
    customer_doc = db.customers.find_one({
        "$or": [
            {"email": sender},
            {"additional_emails": sender}
        ]
    })

    customer_id = customer_doc["_id"] if customer_doc else None

    if customer_found and context.get("customer"):
        customer = context["customer"]
    else:
        customer = {
            "company_name": "Unknown customer",
            "email": sender,
            "note": "No matching customer record found."
        }

    machines = context.get("machines", [])
    cases = context.get("cases", [])
    prior_emails = context.get("emails", [])[:5]
    service_records = context.get("service_records", [])
    orders = context.get("parts_orders", [])
    warranties = context.get("warranties", [])
    appointments = context.get("appointments", [])
    spare_parts = context.get("spare_parts", [])
    inventory = context.get("inventory", [])

    print("\nStep 3: Searching technical documentation...")

    semantic_query = f"""
    Email subject: {subject}

    Customer email: {body}

    Technical issue: {analysis.summary}

    Error codes: {analysis.error_codes}

    Machine model: {analysis.machine_model}
    """

    sources = retrieve_similar_chunks(
        db,
        semantic_query,
        limit=5
    )

    # Add customer's machine records as structured sources.
    for machine in machines:
        sources.append({
            "source_id": str(machine.get("_id")),
            "title": "Customer machine information",
            "text": json.dumps(
                machine,
                default=str,
                ensure_ascii=False
            ),
            "source_type": "machine record",
            "score": 1.0
        })

    # Add previous technical cases.
    for case in cases:
        sources.append({
            "source_id": str(case.get("_id")),
            "title": "Previous technical case",
            "text": json.dumps(
                case,
                default=str,
                ensure_ascii=False
            ),
            "source_type": "case record",
            "score": 1.0
        })

    # Add service history.
    for record in service_records:
        sources.append({
            "source_id": str(record.get("_id")),
            "title": "Previous service record",
            "text": json.dumps(
                record,
                default=str,
                ensure_ascii=False
            ),
            "source_type": "service record",
            "score": 1.0
        })

    print("\nStep 4: Generating suggested response...")

    draft = generate_draft(
        subject=subject,
        body=body,
        customer=customer,
        orders=orders,
        cases=cases,
        prior_emails=prior_emails,
        sources=sources
    )

    print("\nStep 5: Saving email for employee review...")

    email_id = "in_" + uuid.uuid4().hex[:12]

    email_record = {
        "_id": email_id,
        "customer_id": customer_id,
        "gmail_message_id": gmail_message_id,
        "direction": "inbound",
        "sender": sender,
        "sender_name": sender_name,
        "subject": subject,
        "body": body,
        "analysis": analysis.model_dump(),
        "customer_context_found": customer_found,
        "draft": draft,
        "status": "pending_review",
        "created_at": datetime.now(timezone.utc)
    }

    db.emails.insert_one(email_record)

    print("\nEmail processing completed!")

    return {
        "email_id": email_id,
        "customer": customer,
        "customer_found": customer_found,
        "machines": machines,
        "orders": orders,
        "related_cases": cases,
        "prior_emails": prior_emails,
        "service_records": service_records,
        "warranties": warranties,
        "appointments": appointments,
        "spare_parts": spare_parts,
        "inventory": inventory,
        "analysis": analysis.model_dump(),
        "sources": sources,
        "draft": draft,
        "status": "pending_review"
    }
