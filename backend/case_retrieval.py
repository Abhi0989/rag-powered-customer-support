
from datetime import datetime
from bson import ObjectId


def clean_data(data):
    """Convert MongoDB values into JSON-friendly Python values."""

    if isinstance(data, list):
        return [clean_data(item) for item in data]

    if isinstance(data, dict):
        return {
            key: clean_data(value)
            for key, value in data.items()
            if key != "embedding"
        }

    if isinstance(data, ObjectId):
        return str(data)

    if isinstance(data, datetime):
        return data.isoformat()

    return data


def get_customer_context(db, sender_email):
    """
    Find a customer using either the primary email address
    or one of the additional email addresses.
    """

    sender_email = sender_email.strip().lower()

    customer = db.customers.find_one({
        "$or": [
            {"email": sender_email},
            {"additional_emails": sender_email}
        ]
    })

    if not customer:
        return {
            "customer_found": False,
            "customer": None,
            "machines": [],
            "cases": [],
            "emails": [],
            "service_records": [],
            "warranties": [],
            "maintenance_plans": [],
            "machine_readings": [],
            "appointments": [],
            "case_activities": [],
            "parts_orders": [],
            "spare_parts": [],
            "inventory": [],
            "technicians": [],
            "knowledge_documents": [],
            "message": "Customer not found in database."
        }

    customer_id = customer["_id"]

    # Retrieve customer machines
    machines = list(
        db.machines.find({"customer_id": customer_id})
    )

    machine_ids = [
        machine["_id"]
        for machine in machines
    ]

    # Retrieve previous cases
    cases = list(
        db.cases.find(
            {"customer_id": customer_id}
        ).sort("created_at", -1)
    )

    # Retrieve previous emails
    emails = list(
        db.emails.find(
            {"customer_id": customer_id}
        ).sort("created_at", -1)
    )

    # Retrieve service records
    service_records = list(
        db.service_records.find(
            {"customer_id": customer_id}
        ).sort("service_date", -1)
    )

    # Retrieve warranties
    warranties = list(
        db.warranties.find(
            {"customer_id": customer_id}
        )
    )

    # Retrieve maintenance plans
    maintenance_plans = list(
        db.maintenance_plans.find(
            {"customer_id": customer_id}
        )
    )

    # Retrieve machine readings
    machine_readings = []

    if machine_ids:
        machine_readings = list(
            db.machine_readings.find({
                "machine_id": {"$in": machine_ids}
            }).sort("recorded_at", -1)
        )

    # Retrieve service appointments
    appointments = list(
        db.service_appointments.find(
            {"customer_id": customer_id}
        ).sort("appointment_date", -1)
    )

    # Retrieve activities related to previous cases
    case_ids = [
        case["_id"]
        for case in cases
    ]

    case_activities = []

    if case_ids:
        case_activities = list(
            db.case_activities.find({
                "case_id": {"$in": case_ids}
            }).sort("created_at", -1)
        )

    # Retrieve parts orders
    parts_orders = []

    if case_ids:
        parts_orders = list(
            db.parts_orders.find({
                "case_id": {"$in": case_ids}
            })
        )

    # Retrieve spare parts
    part_ids = list({
        order["part_id"]
        for order in parts_orders
        if order.get("part_id")
    })

    spare_parts = []

    if part_ids:
        spare_parts = list(
            db.spare_parts.find({
                "_id": {"$in": part_ids}
            })
        )

    # Retrieve inventory information
    inventory = []

    if part_ids:
        inventory = list(
            db.inventory.find({
                "part_id": {"$in": part_ids}
            })
        )

    # Retrieve technicians assigned to appointments
    technician_ids = list({
        appointment["technician_id"]
        for appointment in appointments
        if appointment.get("technician_id")
    })

    technicians = []

    if technician_ids:
        technicians = list(
            db.technicians.find({
                "_id": {"$in": technician_ids}
            })
        )

    # Retrieve technical documents for customer's machine models
    machine_models = [
        machine.get("model")
        for machine in machines
        if machine.get("model")
    ]

    knowledge_documents = []

    if machine_models:
        knowledge_documents = list(
            db.knowledge_chunks.find({
                "machine_model": {"$in": machine_models}
            })
        )

    # Retrieve general technical policies
    general_policies = list(
        db.knowledge_chunks.find({
            "machine_model": {"$exists": False}
        })
    )

    knowledge_documents.extend(general_policies)

    # Combine all customer information
    context = {
        "customer_found": True,
        "customer": customer,
        "machines": machines,
        "cases": cases,
        "emails": emails,
        "service_records": service_records,
        "warranties": warranties,
        "maintenance_plans": maintenance_plans,
        "machine_readings": machine_readings,
        "appointments": appointments,
        "case_activities": case_activities,
        "parts_orders": parts_orders,
        "spare_parts": spare_parts,
        "inventory": inventory,
        "technicians": technicians,
        "knowledge_documents": knowledge_documents
    }

    return clean_data(context)
