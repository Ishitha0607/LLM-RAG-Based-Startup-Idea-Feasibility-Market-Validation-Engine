import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import pickle

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "processed" / "startup_ideas.csv"
OUTPUT_DIR = BASE_DIR / "embeddings"
OUTPUT_FILE = OUTPUT_DIR / "startup_embeddings.pkl"


MODEL_NAME = "all-MiniLM-L6-v2"


def load_dataset():
    """Load the processed startup ideas dataset."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE)

    print(f"Dataset loaded successfully.")
    print(f"Number of records: {len(df)}")

    return df


def prepare_text(row):
    """
    Combine important information from one startup
    problem record into a single text document.
    """

    text = f"""
Market: {row['market']}
Problem: {row['problem']}
Signal Source: {row['signal_source']}
Edition: {row['edition']}
""".strip()
    return text


def generate_embeddings():
    print("=" * 70)
    print("STARTUP IDEA EMBEDDING GENERATOR")
    print("=" * 70)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_dataset()
    print("\nPreparing text documents...")

    documents = []
    for _, row in df.iterrows():
        document = prepare_text(row)
        documents.append(document)

    print(f"Documents prepared: {len(documents)}")

    print("\nLoading Sentence Transformer model...")
    print(f"Model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded successfully.")

    print("\nGenerating embeddings...")
    print("This may take some time on the first run.")

    embeddings = model.encode(documents, show_progress_bar=True, convert_to_numpy=True)

    print("\nEmbeddings generated successfully.")

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {embeddings.shape[1]}")

    embedding_data = []

    for index, row in df.iterrows():
        embedding_data.append(
            {
                "id": int(row["id"]),
                "edition": row["edition"],
                "market": row["market"],
                "problem": row["problem"],
                "signal_source": row["signal_source"],
                "source_url": row["source_url"],
                "document": documents[index],
                "embedding": embeddings[index],
            }
        )

    with open(OUTPUT_FILE, "wb") as file:
        pickle.dump(embedding_data, file)

    print("\nEmbeddings saved successfully.")

    print(f"Output file:")
    print(OUTPUT_FILE)

    print("\n" + "=" * 70)
    print("EMBEDDING GENERATION COMPLETED")
    print("=" * 70)

    print(f"Records processed : {len(df)}")
    print(f"Embedding model   : {MODEL_NAME}")
    print(f"Vector dimension  : {embeddings.shape[1]}")
    print(f"Saved file        : {OUTPUT_FILE}")

    print("=" * 70)


if __name__ == "__main__":
    generate_embeddings()
