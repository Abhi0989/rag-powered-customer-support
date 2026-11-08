from datetime import datetime, timedelta, timezone
from backend.retrieval import rebuild_knowledge_index

def seed_demo_data(db):
    for name in ["customers", "orders", "cases", "emails", "knowledge_chunks", "audit_logs"]:
        db[name].delete_many({})

    now = datetime.now(timezone.utc)
    customers = [
        {
            "_id": "cust_001", "name": "Anna Müller", "email": "anna.mueller@example.com",
            "phone": "+49 30 5550101", "customer_type": "Business",
            "address": {"city": "Berlin", "country": "Germany"},
            "preferences": {"language": "English"}
        },
        {
            "_id": "cust_002", "name": "Markus Weber", "email": "markus.weber@example.com",
            "phone": "+49 40 5550102", "customer_type": "Private",
            "address": {"city": "Hamburg", "country": "Germany"},
            "preferences": {"language": "German"}
        }
    ]
    db.customers.insert_many(customers)

    orders = [
        {"_id": "ord_45021", "customer_id": "cust_001", "order_number": "45021",
         "status": "Delayed", "placed_at": now - timedelta(days=28),
         "estimated_delivery": (now - timedelta(days=3)).date().isoformat(),
         "tracking_status": "In transit; last carrier scan five days ago",
         "items": [{"sku": "PRD-100", "name": "Business Router", "quantity": 1}],
         "total_eur": 249.00},
        {"_id": "ord_45035", "customer_id": "cust_001", "order_number": "45035",
         "status": "Delivered", "placed_at": now - timedelta(days=10),
         "estimated_delivery": (now - timedelta(days=5)).date().isoformat(),
         "tracking_status": "Delivered",
         "items": [{"sku": "CAB-20", "name": "Network Cable", "quantity": 2}],
         "total_eur": 19.90},
        {"_id": "ord_55110", "customer_id": "cust_002", "order_number": "55110",
         "status": "Delivered", "placed_at": now - timedelta(days=7),
         "estimated_delivery": (now - timedelta(days=2)).date().isoformat(),
         "tracking_status": "Delivered",
         "items": [{"sku": "MON-24", "name": "24-inch Monitor", "quantity": 1}],
         "total_eur": 179.00}
    ]
    db.orders.insert_many(orders)

    cases = [
        {"_id": "case_1001", "customer_id": "cust_001", "order_id": "ord_45021",
         "status": "Open", "category": "Delivery", "priority": "High",
         "summary": "Customer previously reported that tracking had stopped updating.",
         "resolution": None, "updated_at": now - timedelta(days=2)},
        {"_id": "case_1002", "customer_id": "cust_001", "order_id": "ord_45035",
         "status": "Closed", "category": "Billing", "priority": "Normal",
         "summary": "Customer asked for an invoice copy.",
         "resolution": "Invoice PDF was sent to the customer.", "updated_at": now - timedelta(days=6)},
        {"_id": "case_2001", "customer_id": "cust_002", "order_id": "ord_55110",
         "status": "Closed", "category": "Product", "priority": "Normal",
         "summary": "Customer asked about monitor compatibility.",
         "resolution": "Compatibility information was provided.", "updated_at": now - timedelta(days=3)}
    ]
    db.cases.insert_many(cases)

    emails = [
        {"_id": "email_old_1", "customer_id": "cust_001", "case_id": "case_1001",
         "direction": "outbound", "subject": "We are checking your delivery",
         "body": "Our logistics team has been asked to investigate the missing carrier scan. We do not yet have a confirmed delivery date.",
         "created_at": now - timedelta(days=2)},
        {"_id": "email_old_2", "customer_id": "cust_001", "case_id": "case_1002",
         "direction": "outbound", "subject": "Your invoice",
         "body": "We sent the invoice PDF for order 45035.",
         "created_at": now - timedelta(days=6)}
    ]
    db.emails.insert_many(emails)

    docs = [
        {"_id": "doc_1", "title": "Delivery support policy",
         "text": "For delayed shipments, verify the latest carrier scan and order status. If tracking has not changed for more than 72 hours, create or update a logistics investigation. Do not promise a delivery date unless the carrier confirms one. Keep the customer informed.",
         "source_type": "policy"},
        {"_id": "doc_2", "title": "Refund and replacement policy",
         "text": "A replacement or refund must not be promised until the order and investigation outcome have been checked. Escalate damaged or lost shipments to the support team for review.",
         "source_type": "policy"},
        {"_id": "doc_3", "title": "Invoice support policy",
         "text": "Invoice discrepancies should be checked against the original quotation, order total and invoice. If these documents do not agree, route the case to the billing team. Do not confirm a refund without billing approval.",
         "source_type": "policy"}
    ]
    db.knowledge_chunks.insert_many(docs)
    rebuild_knowledge_index(db)
