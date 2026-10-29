import pickle
from pathlib import Path

import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDING_FILE = BASE_DIR / "embeddings" / "startup_embeddings.pkl"

CHROMA_DIR = BASE_DIR / "rag" / "chroma_db"
COLLECTION_NAME = "startup_ideas"


def load_embeddings():
    """Load the generated startup embeddings."""

    if not EMBEDDING_FILE.exists():
        raise FileNotFoundError(f"Embedding file not found: {EMBEDDING_FILE}")

    with open(EMBEDDING_FILE, "rb") as file:
        data = pickle.load(file)

    print(f"Loaded {len(data)} embedding records.")

    return data


def create_vector_store():
    print("=" * 70)
    print("STARTUP IDEA CHROMADB VECTOR STORE")
    print("=" * 70)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    print("\nInitializing ChromaDB...")
    print(f"Database location: {CHROMA_DIR}")

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Startup problem and opportunity knowledge base"},
    )

    print(f"Collection: {COLLECTION_NAME}")

    embedding_data = load_embeddings()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for record in embedding_data:
        ids.append(str(record["id"]))
        documents.append(record["document"])
        # Convert NumPy array to normal Python list
        embeddings.append(record["embedding"].tolist())

        metadatas.append(
            {
                "edition": str(record["edition"]),
                "market": str(record["market"]),
                "problem": str(record["problem"]),
                "signal_source": (
                    ""
                    if record["signal_source"] is None
                    else str(record["signal_source"])
                ),
                "source_url": (
                    "" if record["source_url"] is None else str(record["source_url"])
                ),
            }
        )

    print("\nAdding records to ChromaDB...")

    collection.upsert(
        ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas
    )

    total_records = collection.count()

    print("\n" + "=" * 70)
    print("VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 70)

    print(f"Collection       : {COLLECTION_NAME}")
    print(f"Records stored   : {total_records}")
    print(f"Database path    : {CHROMA_DIR}")

    print("=" * 70)


if __name__ == "__main__":
    create_vector_store()
