from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# =========================================================
# BASE CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "rag" / "chroma_db"

COLLECTION_NAME = "startup_ideas"

MODEL_NAME = "all-MiniLM-L6-v2"


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


# =========================================================
# LOAD CHROMADB
# =========================================================

client = chromadb.PersistentClient(path=str(CHROMA_DIR))


# =========================================================
# LOAD COLLECTION
# =========================================================

try:

    collection = client.get_collection(name=COLLECTION_NAME)

    print(f"ChromaDB collection loaded: " f"{COLLECTION_NAME}")

    print(f"Records available: " f"{collection.count()}")

except Exception as e:

    raise RuntimeError(
        f"Unable to load ChromaDB collection " f"'{COLLECTION_NAME}': {str(e)}"
    )


# =========================================================
# SEMANTIC SEARCH
# =========================================================


def search_startup_ideas(query, top_k=5):
    """
    Search the startup knowledge base using
    semantic similarity.

    Returns a list of dictionaries containing:

        document
        metadata
        distance
    """

    # -----------------------------------------------------
    # VALIDATE QUERY
    # -----------------------------------------------------

    if not query:

        return []

    if not isinstance(query, str):

        query = str(query)

    query = query.strip()

    if not query:

        return []

    # -----------------------------------------------------
    # VALIDATE TOP K
    # -----------------------------------------------------

    try:

        top_k = int(top_k)

    except (TypeError, ValueError):

        top_k = 5

    if top_k <= 0:

        top_k = 5

    # -----------------------------------------------------
    # GET AVAILABLE RECORD COUNT
    # -----------------------------------------------------

    try:

        record_count = collection.count()

    except Exception as e:

        print(f"ChromaDB count error: {str(e)}")

        return []

    if record_count == 0:

        print("ChromaDB collection contains no records.")

        return []

    # Never request more records than available
    top_k = min(top_k, record_count)

    # -----------------------------------------------------
    # CREATE QUERY EMBEDDING
    # -----------------------------------------------------

    try:

        query_embedding = model.encode([query], convert_to_numpy=True)[0].tolist()

    except Exception as e:

        print(f"Embedding generation failed: {str(e)}")

        return []

    # -----------------------------------------------------
    # SEARCH CHROMADB
    # -----------------------------------------------------

    try:

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    except Exception as e:

        print(f"ChromaDB search failed: {str(e)}")

        return []

    # -----------------------------------------------------
    # EXTRACT RESULTS
    # -----------------------------------------------------

    documents = results.get("documents", [[]])

    metadatas = results.get("metadatas", [[]])

    distances = results.get("distances", [[]])

    # ChromaDB returns nested lists
    documents = documents[0] if documents else []

    metadatas = metadatas[0] if metadatas else []

    distances = distances[0] if distances else []

    # -----------------------------------------------------
    # BUILD STANDARD RESULT FORMAT
    # -----------------------------------------------------

    retrieved_results = []

    for document, metadata, distance in zip(documents, metadatas, distances):

        if metadata is None:

            metadata = {}

        retrieved_results.append(
            {"document": document, "metadata": metadata, "distance": distance}
        )

    return retrieved_results


# =========================================================
# DISPLAY SEARCH RESULTS
# =========================================================


def display_results(query, results):

    print("\n" + "=" * 70)

    print("SEMANTIC SEARCH RESULTS")

    print("=" * 70)

    print("\nQuery:")

    print(query)

    if not results:

        print("\nNo matching results found.")

        return

    for index, result in enumerate(results, start=1):

        metadata = result.get("metadata", {})

        print("\n" + "-" * 70)

        print(f"Result {index}")

        print(f"Market         : " f"{metadata.get('market', '')}")

        print(f"Edition        : " f"{metadata.get('edition', '')}")

        print(f"Signal Source  : " f"{metadata.get('signal_source', '')}")

        distance = result.get("distance")

        if distance is not None:

            try:

                print(f"Similarity Distance: " f"{float(distance):.4f}")

            except (TypeError, ValueError):

                print(f"Similarity Distance: " f"{distance}")

        print("\nProblem:")

        print(metadata.get("problem", ""))

        print("\nSource URL:")

        print(metadata.get("source_url", ""))

    print("\n" + "=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    test_query = (
        "An AI tool that helps accounting firms "
        "automatically process invoices and reduce "
        "manual financial data entry."
    )

    results = search_startup_ideas(test_query, top_k=5)

    display_results(test_query, results)
