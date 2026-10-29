import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "processed" / "startup_ideas.csv"


def validate_dataset():
    print("=" * 70)
    print("STARTUP IDEA DATA VALIDATION")
    print("=" * 70)

    # Check file
    if not CSV_FILE.exists():
        print("ERROR: startup_ideas.csv not found.")
        return

    # Load dataset
    df = pd.read_csv(CSV_FILE)

    print(f"\nDataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

    print("\nColumns:")
    for column in df.columns:
        print(f"  ✓ {column}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nRecords by edition:")
    print(df["edition"].value_counts().sort_index())

    print("\nRecords by market:")

    market_counts = df["market"].value_counts()

    for market, count in market_counts.items():
        print(f"  {market}: {count}")

    duplicate_problems = df.duplicated(subset=["market", "problem"], keep=False)

    print("\nDuplicate market + problem records:")
    print(duplicate_problems.sum())

    empty_problems = df["problem"].isna() | (
        df["problem"].astype(str).str.strip() == ""
    )

    print("\nEmpty problem records:")
    print(empty_problems.sum())

    empty_markets = df["market"].isna() | (df["market"].astype(str).str.strip() == "")

    print("\nEmpty market records:")
    print(empty_markets.sum())

    missing_urls = df["source_url"].isna() | (
        df["source_url"].astype(str).str.strip() == ""
    )

    print("\nMissing source URLs:")
    print(missing_urls.sum())

    if missing_urls.sum() > 0:
        print("\nRecords without source URLs:")
        print(
            df.loc[
                missing_urls, ["id", "edition", "market", "problem", "signal_source"]
            ].to_string(index=False)
        )

    missing_signals = df["signal_source"].isna() | (
        df["signal_source"].astype(str).str.strip() == ""
    )

    print("\nMissing signal sources:")
    print(missing_signals.sum())

    print("\nSample records:")
    print(
        df[["id", "edition", "market", "problem", "signal_source", "source_url"]]
        .head(5)
        .to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    validate_dataset()
