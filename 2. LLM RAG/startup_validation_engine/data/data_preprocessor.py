import re
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
OUTPUT_FILE = PROCESSED_DIR / "startup_ideas.csv"


def extract_ideas_from_markdown(file_path):
    """
    Extract market, problem, signal source and source URL
    from one monthly startup-ideas Markdown file.
    """
    text = file_path.read_text(encoding="utf-8")
    # Extract edition from filename
    edition = file_path.stem
    records = []
    current_market = None
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        market_match = re.match(r"^##\s+(.+?)\s*$", line)

        if market_match:
            market = market_match.group(1).strip()

            # Ignore non-market headings
            ignored_headings = {"Jump to a market", "How to read this list"}

            if market not in ignored_headings:
                current_market = market
            continue

        if current_market and line.startswith("|") and line.endswith("|"):
            columns = [column.strip() for column in line.strip("|").split("|")]

            # We need at least 2 columns:
            # Problem | Signal
            if len(columns) < 2:
                continue
            problem = columns[0]

            # Skip Markdown table headers
            if problem.lower() in {"problem", "market", "---"}:
                continue

            # Skip separator rows
            if re.fullmatch(r"[-:\s]+", problem):
                continue

            signal = columns[1]
            signal_match = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", signal)

            if signal_match:
                signal_source = signal_match.group(1).strip()
                source_url = signal_match.group(2).strip()
            else:
                # Some records may contain plain text instead
                signal_source = re.sub(r"`", "", signal).strip()
                source_url = ""

            # Ignore empty or invalid problem rows
            if not problem or problem.startswith("---"):
                continue

            records.append(
                {
                    "edition": edition,
                    "market": current_market,
                    "problem": problem,
                    "signal_source": signal_source,
                    "source_url": source_url,
                }
            )

    return records


def process_all_files():
    print("=" * 70)
    print("STARTUP IDEA DATA PREPROCESSOR")
    print("=" * 70)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    markdown_files = sorted(RAW_DIR.glob("*.md"))

    if not markdown_files:
        print("ERROR: No Markdown files found in data/raw/")
        return

    all_records = []
    for file_path in markdown_files:
        print(f"\nProcessing: {file_path.name}")
        records = extract_ideas_from_markdown(file_path)
        print(f"Extracted records: {len(records)}")
        all_records.extend(records)

    unique_records = []
    seen = set()
    for record in all_records:
        key = (record["edition"], record["market"], record["problem"])

        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    duplicates_removed = len(all_records) - len(unique_records)
    fieldnames = ["id", "edition", "market", "problem", "signal_source", "source_url"]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for index, record in enumerate(unique_records, start=1):
            writer.writerow(
                {
                    "id": index,
                    "edition": record["edition"],
                    "market": record["market"],
                    "problem": record["problem"],
                    "signal_source": record["signal_source"],
                    "source_url": record["source_url"],
                }
            )

    print("\n" + "=" * 70)
    print("PROCESSING COMPLETED")
    print("=" * 70)

    print(f"Total records extracted : {len(all_records)}")
    print(f"Duplicates removed      : {duplicates_removed}")
    print(f"Final records            : {len(unique_records)}")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)

    print("=" * 70)


if __name__ == "__main__":
    process_all_files()
