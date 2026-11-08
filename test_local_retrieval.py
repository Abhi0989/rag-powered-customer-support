
from backend.db import get_db
from backend.retrieval import (
    rebuild_knowledge_index,
    retrieve_similar_chunks
)


def main():

    db = get_db()

    print("\nGenerating local knowledge embeddings...\n")

    rebuild_knowledge_index(db)

    print("\nTesting semantic search...\n")

    query = """
    Our CNC machine stopped during production.
    The control panel displays error E-204.
    """

    results = retrieve_similar_chunks(
        db,
        query,
        limit=5
    )

    print("SEARCH RESULTS:\n")

    for result in results:

        print("TITLE:", result["title"])
        print("SOURCE:", result["source_type"])
        print("SIMILARITY:", round(result["score"], 4))
        print("CONTENT:", result["text"])
        print("-" * 60)

    print("\nLOCAL RAG TEST COMPLETED!")


if __name__ == "__main__":
    main()
