import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

BASE_DIR = Path(__file__).resolve().parent.parent

# Make sure "rag.retriever" can be imported no matter how this file
# is run (e.g. `python rag/rag_pipeline.py` vs `python -m rag.rag_pipeline`).
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from rag.retriever import search_startup_ideas

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. " "Please add it to the .env file.")

MODEL_NAME = "gemini-2.5-flash"

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)


def build_context(results):
    """
    Convert retrieved startup problems into a context
    that can be provided to Gemini.
    """
    context_parts = []

    for index, result in enumerate(results, start=1):

        metadata = result["metadata"]

        context = f"""
        Evidence {index}

        Market:
        {metadata.get("market", "")}

        Problem:
        {metadata.get("problem", "")}

        Edition:
        {metadata.get("edition", "")}

        Signal Source:
        {metadata.get("signal_source", "")}

        Source URL:
        {metadata.get("source_url", "")}
        """.strip()

        context_parts.append(context)
    return "\n\n".join(context_parts)


def analyze_startup_idea(startup_idea, top_k=5):
    print("\nRetrieving relevant evidence...")
    results = search_startup_ideas(startup_idea, top_k=top_k)

    if not results:
        return {"analysis": "No relevant evidence was found.", "sources": []}

    context = build_context(results)
    prompt = f"""
    You are a startup market validation assistant.

    Analyze the following startup idea using ONLY the
    retrieved evidence provided below as the primary
    supporting information.

    STARTUP IDEA:
    {startup_idea}

    RETRIEVED EVIDENCE:
    {context}

    Provide a concise preliminary analysis with these sections:

    1. Problem Relevance
    2. Market Relevance
    3. Evidence-Based Opportunity
    4. Potential Concerns
    5. Initial Validation Recommendation

    Important instructions:

    - Clearly distinguish evidence from interpretation.
    - Do not invent statistics, companies, market sizes,
    customer numbers, or facts that are not present
    in the retrieved evidence.
    - If the evidence is insufficient, explicitly say so.
    - Mention the relevant evidence when making a claim.
    - Do not treat the retrieved problems as proof that
    the proposed startup will succeed.
    """
    print("\nSending retrieved evidence to Gemini...")

    response = llm.invoke(prompt)
    analysis = response.content
    sources = []

    for result in results:
        metadata = result["metadata"]
        sources.append(
            {
                "market": metadata.get("market", ""),
                "problem": metadata.get("problem", ""),
                "edition": metadata.get("edition", ""),
                "signal_source": metadata.get("signal_source", ""),
                "source_url": metadata.get("source_url", ""),
                "distance": result["distance"],
            }
        )

    return {"analysis": analysis, "sources": sources}


def display_analysis(startup_idea, result):
    print("\n")
    print("=" * 70)
    print("LLM-RAG STARTUP ANALYSIS")
    print("=" * 70)

    print("\nSTARTUP IDEA:")
    print(startup_idea)

    print("\n" + "-" * 70)
    print("GEMINI ANALYSIS")
    print("-" * 70)

    print(result["analysis"])

    print("\n" + "-" * 70)
    print("SUPPORTING EVIDENCE")
    print("-" * 70)

    for index, source in enumerate(result["sources"], start=1):
        print(f"\nEvidence {index}")
        print(f"Market        : {source['market']}")
        print(f"Edition       : {source['edition']}")
        print(f"Problem       : {source['problem']}")
        print(f"Signal Source : {source['signal_source']}")
        print(f"Source URL    : {source['source_url']}")
        print(f"Distance      : " f"{source['distance']:.4f}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_startup_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    result = analyze_startup_idea(test_startup_idea, top_k=5)

    display_analysis(test_startup_idea, result)
