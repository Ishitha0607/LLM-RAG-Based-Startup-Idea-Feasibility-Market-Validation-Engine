from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from rag.retriever import search_startup_ideas


class CustomerPainAgent:
    """
    Identifies customer pain points from evidence retrieved
    from the startup knowledge base.
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
                "pain_points": [],
                "evidence_count": 0,
                "pain_categories": [],
                "evidence_strength": "Insufficient",
                "message": "No relevant customer pain evidence found.",
            }

        pain_points = []
        categories = []

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
                word in problem_lower
                for word in ["manual", "re-enter", "key in", "data entry"]
            ):
                category = "Manual Work"

            elif any(
                word in problem_lower
                for word in ["error", "errors", "error-prone", "mistake"]
            ):
                category = "Errors"

            elif any(
                word in problem_lower for word in ["delay", "delayed", "time", "hours"]
            ):
                category = "Time and Delays"

            elif any(
                word in problem_lower for word in ["integration", "software", "sync"]
            ):
                category = "Software Integration"

            else:
                category = "Operational Problem"

            if category not in categories:
                categories.append(category)

            pain_points.append(
                {
                    "pain_point": problem,
                    "category": category,
                    "market": market,
                    "edition": edition,
                    "signal_source": signal_source,
                    "source_url": source_url,
                    "distance": result["distance"],
                }
            )

        evidence_count = len(pain_points)

        if evidence_count >= 5:
            evidence_strength = "Strong"
        elif evidence_count >= 3:
            evidence_strength = "Moderate"
        elif evidence_count >= 1:
            evidence_strength = "Limited"
        else:
            evidence_strength = "Insufficient"

        return {
            "startup_idea": startup_idea,
            "pain_points": pain_points,
            "pain_categories": categories,
            "evidence_count": evidence_count,
            "evidence_strength": evidence_strength,
        }


def display_pain_analysis(result):
    print("\n")
    print("=" * 70)
    print("CUSTOMER PAIN-POINT AGENT")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\nEvidence Strength:")
    print(result["evidence_strength"])

    print("\nPain Categories:")

    for category in result["pain_categories"]:
        print(f"  - {category}")

    print("\nIdentified Customer Pain Points:")

    for index, pain in enumerate(result["pain_points"], start=1):
        print("\n" + "-" * 70)

        print(f"Pain Point {index}")
        print(f"Category      : {pain['category']}")
        print(f"Market        : {pain['market']}")
        print(f"Edition       : {pain['edition']}")

        print("\nProblem:")
        print(pain["pain_point"])

        print(f"\nSignal Source : {pain['signal_source']}")
        print(f"Distance      : {pain['distance']:.4f}")

        print("\nSource URL:")
        print(pain["source_url"])

    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    agent = CustomerPainAgent(top_k=5)
    result = agent.analyze(test_idea)
    display_pain_analysis(result)
