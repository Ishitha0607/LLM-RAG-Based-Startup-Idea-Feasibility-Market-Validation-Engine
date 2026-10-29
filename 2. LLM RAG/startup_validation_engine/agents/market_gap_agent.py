from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from rag.retriever import search_startup_ideas


class MarketGapAgent:
    """
    Identifies potential unresolved market gaps from
    evidence retrieved from the RAG knowledge base.

    The agent does NOT claim that a market gap definitely
    exists. It identifies evidence-supported gaps and
    clearly reports evidence limitations.
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
                "unresolved_problems": [],
                "potential_market_gaps": [],
                "gap_evidence_status": "Insufficient",
                "research_limitations": ["No relevant evidence was retrieved."],
            }

        unresolved_problems = []
        potential_gaps = []

        for result in results:

            metadata = result["metadata"]

            problem = metadata.get("problem", "")
            market = metadata.get("market", "")
            edition = metadata.get("edition", "")
            signal_source = metadata.get("signal_source", "")
            source_url = metadata.get("source_url", "")

            if not problem:
                continue

            problem_lower = problem.lower()

            if any(
                term in problem_lower
                for term in [
                    "manual",
                    "manually",
                    "re-enter",
                    "reconcile",
                    "key in",
                    "data entry",
                ]
            ):

                unresolved_problems.append(
                    {
                        "problem": problem,
                        "market": market,
                        "edition": edition,
                        "signal_source": signal_source,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

                potential_gaps.append(
                    {
                        "type": "Workflow Automation Gap",
                        "description": (
                            "The retrieved evidence indicates that "
                            "customers are still performing manual "
                            "data-entry or reconciliation work."
                        ),
                        "supporting_problem": problem,
                        "market": market,
                        "edition": edition,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

            elif any(
                term in problem_lower
                for term in [
                    "integration",
                    "integrated",
                    "software",
                    "application",
                    "sync",
                ]
            ):

                unresolved_problems.append(
                    {
                        "problem": problem,
                        "market": market,
                        "edition": edition,
                        "signal_source": signal_source,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

                potential_gaps.append(
                    {
                        "type": "Integration Gap",
                        "description": (
                            "The evidence indicates difficulties "
                            "connecting or coordinating existing "
                            "software systems."
                        ),
                        "supporting_problem": problem,
                        "market": market,
                        "edition": edition,
                        "source_url": source_url,
                        "distance": result["distance"],
                    }
                )

        unique_gaps = []
        seen = set()

        for gap in potential_gaps:

            key = (gap["type"], gap["supporting_problem"])

            if key not in seen:

                seen.add(key)
                unique_gaps.append(gap)

        potential_gaps = unique_gaps

        gap_count = len(potential_gaps)

        if gap_count >= 4:

            gap_evidence_status = "Strong Evidence of Unresolved Problems"

        elif gap_count >= 2:

            gap_evidence_status = "Moderate Evidence of Unresolved Problems"

        elif gap_count == 1:

            gap_evidence_status = "Limited Evidence"

        else:

            gap_evidence_status = "Insufficient Evidence"

        research_limitations = [
            "The dataset does not directly measure market size.",
            "The dataset does not provide customer willingness-to-pay data.",
            "The dataset does not prove that competitors cannot solve the identified problems.",
            "A recurring problem is evidence of an unresolved need, not proof of a market gap.",
        ]

        return {
            "startup_idea": startup_idea,
            "evidence_count": len(results),
            "unresolved_problems": unresolved_problems,
            "potential_market_gaps": potential_gaps,
            "gap_evidence_status": gap_evidence_status,
            "research_limitations": research_limitations,
        }


def display_gap_analysis(result):

    print("\n")
    print("=" * 70)
    print("MARKET GAP ANALYSIS AGENT")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\nGap Evidence Status:")
    print(result["gap_evidence_status"])

    print("\nUnresolved Problems:")

    if not result["unresolved_problems"]:

        print("  No unresolved problems identified.")

    else:

        for index, problem in enumerate(result["unresolved_problems"], start=1):

            print("\n" + "-" * 70)

            print(f"Problem {index}")
            print(f"Market        : {problem['market']}")
            print(f"Edition       : {problem['edition']}")

            print("\nProblem:")
            print(problem["problem"])

            print(f"\nSignal Source : " f"{problem['signal_source']}")

            print(f"Distance      : " f"{problem['distance']:.4f}")

            print("\nSource URL:")
            print(problem["source_url"])

    print("\n" + "-" * 70)
    print("POTENTIAL MARKET GAPS")
    print("-" * 70)

    if not result["potential_market_gaps"]:

        print("\nNo potential gaps identified.")

    else:

        for index, gap in enumerate(result["potential_market_gaps"], start=1):

            print(f"\nGap {index}")
            print(f"Type        : {gap['type']}")

            print("\nDescription:")
            print(gap["description"])

            print("\nSupporting Problem:")
            print(gap["supporting_problem"])

            print(f"\nMarket      : {gap['market']}")
            print(f"Edition     : {gap['edition']}")

            print("\nSource URL:")
            print(gap["source_url"])

    print("\n" + "-" * 70)
    print("RESEARCH LIMITATIONS")
    print("-" * 70)

    for limitation in result["research_limitations"]:

        print(f"\n- {limitation}")

    print("\n" + "=" * 70)


if __name__ == "__main__":

    test_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    agent = MarketGapAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_gap_analysis(result)
