
from backend.db import get_db


def test_connection():

    db = get_db()

    print("MongoDB connected successfully!")
    print("Database name:", db.name)

    print("\nAvailable collections:")

    for collection in db.list_collection_names():
        print("-", collection)

    print("\nCustomer records:")

    customers = db.customers.find(
        {},
        {"_id": 1, "company_name": 1, "email": 1}
    )

    for customer in customers:
        print(customer)


if __name__ == "__main__":
    test_connection()
