from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from rag.retriever import search_startup_ideas


class CompetitorAgent:
    """
    Performs an initial competitor/solution analysis using
    evidence retrieved from the RAG knowledge base.

    Note:
    The current dataset is primarily a startup-problem and
    market-signal dataset, not a dedicated competitor
    database. Therefore, this agent does not invent
    competitor names.
    """

    def __init__(self, top_k=5):
        self.top_k = top_k

    def analyze(self, startup_idea):

        if not startup_idea or not startup_idea.strip():
            raise ValueError("Startup idea cannot be empty.")

        results = search_startup_ideas(startup_idea, top_k=self.top_k)

        if not results:
            return {
                "startup_idea": startup_idea,
                "evidence_count": 0,
                "solution_signals": [],
                "markets_found": [],
                "existing_solution_evidence": [],
                "specific_competitors": [],
                "competitor_evidence_status": "Insufficient",
                "message": ("No relevant solution or competitor " "evidence found."),
            }

        solution_signals = []
        markets = []
        existing_solution_evidence = []

        for result in results:

            metadata = result["metadata"]

            problem = metadata.get("problem", "")
            market = metadata.get("market", "")
            edition = metadata.get("edition", "")
            signal_source = metadata.get("signal_source", "")
            source_url = metadata.get("source_url", "")

            if market and market not in markets:
                markets.append(market)

            problem_lower = problem.lower()

            solution_terms = [
                "software",
                "application",
                "applications",
                "system",
                "platform",
                "integration",
                "integrated",
                "accounting software",
                "gradebook",
                "communication apps",
            ]

            detected_terms = []

            for term in solution_terms:

                if term in problem_lower:
                    detected_terms.append(term)

            if detected_terms:

                existing_solution_evidence.append(
                    {
                        "problem": problem,
                        "market": market,
                        "edition": edition,
                        "detected_terms": detected_terms,
                        "signal_source": signal_source,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

                solution_signals.append(
                    {
                        "market": market,
                        "edition": edition,
                        "problem": problem,
                        "detected_terms": detected_terms,
                        "signal_source": signal_source,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

        evidence_count = len(results)

        if len(existing_solution_evidence) >= 3:

            competitor_evidence_status = "Moderate"

        elif len(existing_solution_evidence) >= 1:

            competitor_evidence_status = "Limited"

        else:

            competitor_evidence_status = "Insufficient"

        return {
            "startup_idea": startup_idea,
            "evidence_count": evidence_count,
            "solution_signals": solution_signals,
            "markets_found": markets,
            "existing_solution_evidence": existing_solution_evidence,
            "specific_competitors": [],
            "competitor_evidence_status": competitor_evidence_status,
            "message": (
                "No specific competitor names are claimed "
                "because the current dataset does not contain "
                "a dedicated competitor database."
            ),
        }


def display_competitor_analysis(result):

    print("\n")
    print("=" * 70)
    print("COMPETITOR ANALYSIS AGENT")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\nMarkets Found:")

    for market in result["markets_found"]:
        print(f"  - {market}")

    print("\nCompetitor Evidence Status:")
    print(result["competitor_evidence_status"])

    print("\nSpecific Competitor Names:")

    if result["specific_competitors"]:
        for competitor in result["specific_competitors"]:
            print(f"  - {competitor}")
    else:
        print("  None identified from current dataset.")

    print("\nSolution / Existing-System Signals:")

    if not result["solution_signals"]:

        print("  No relevant solution signals found.")

    else:

        for index, signal in enumerate(result["solution_signals"], start=1):

            print("\n" + "-" * 70)

            print(f"Signal {index}")
            print(f"Market        : {signal['market']}")
            print(f"Edition       : {signal['edition']}")

            print(f"Detected Terms: " f"{', '.join(signal['detected_terms'])}")

            print("\nProblem:")
            print(signal["problem"])

            print(f"\nSignal Source : " f"{signal['signal_source']}")

            print(f"Distance      : " f"{signal['distance']:.4f}")

            print("\nSource URL:")
            print(signal["source_url"])

    print("\n" + "-" * 70)
    print("IMPORTANT LIMITATION")
    print("-" * 70)

    print(
        "\nThe current 305-record dataset contains market "
        "problems and signals rather than a dedicated "
        "competitor database."
    )

    print(
        "\nTherefore, this agent does not invent competitor "
        "names or claim that a retrieved company is a "
        "competitor without supporting evidence."
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":

    test_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    agent = CompetitorAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_competitor_analysis(result)
