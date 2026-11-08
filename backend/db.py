
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

_client = None


def get_db():
    global _client

    # Establish connection only once
    if _client is None:

        mongo_uri = os.getenv(
            "MONGODB_URI",
            "mongodb://localhost:27017"
        )

        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000
        )

        # Verify MongoDB connection
        _client.admin.command("ping")

    database_name = os.getenv(
        "MONGODB_DATABASE",
        "email_case_assistant"
    )

    return _client[database_name]


def close_connection():
    global _client

    if _client is not None:
        _client.close()
        _client = None
