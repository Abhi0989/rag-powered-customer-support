from datetime import datetime, timezone

def save_review_decision(db, email_id, decision, edited_draft):
    if decision not in {"approved", "rejected"}:
        raise ValueError("Unsupported review decision")
    email = db.emails.find_one({"_id": email_id})
    if not email:
        raise ValueError("Email record not found")

    db.emails.update_one(
        {"_id": email_id},
        {"$set": {
            "status": decision,
            "reviewed_draft": edited_draft,
            "reviewed_at": datetime.now(timezone.utc)
        }}
    )
    db.audit_logs.insert_one({
        "email_id": email_id, "decision": decision,
        "draft": edited_draft, "created_at": datetime.now(timezone.utc),
        "actor": "demo_employee"
    })
