
import os
import numpy as np
import ollama


def get_embedding(text):
    """
    Generate a local embedding using Ollama.
    """

    model = os.getenv(
        "EMBEDDING_MODEL",
        "nomic-embed-text"
    )

    response = ollama.embed(
        model=model,
        input=text
    )

    return response["embeddings"][0]


def rebuild_knowledge_index(db):
    """
    Generate and store embeddings for all knowledge documents.
    """

    documents = list(db.knowledge_chunks.find({}))

    if not documents:
        print("No knowledge documents found.")
        return

    for doc in documents:

        text = doc.get("title", "") + "\n" + doc.get("text", "")

        vector = get_embedding(text)

        db.knowledge_chunks.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "embedding": vector,
                    "embedding_model": os.getenv(
                        "EMBEDDING_MODEL",
                        "nomic-embed-text"
                    )
                }
            }
        )

    print(f"Successfully indexed {len(documents)} knowledge documents.")


def cosine_similarity(vector_a, vector_b):

    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def retrieve_similar_chunks(db, query, limit=5):
    """
    Retrieve the most relevant technical documents.
    """

    query_vector = get_embedding(query)

    documents = list(
        db.knowledge_chunks.find({
            "embedding": {"$exists": True}
        })
    )

    results = []

    for doc in documents:

        score = cosine_similarity(
            query_vector,
            doc["embedding"]
        )

        results.append({
            "source_id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "text": doc.get("text", ""),
            "source_type": doc.get("source_type", "document"),
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]
