from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from rag.retriever import search_startup_ideas


class MarketAgent:
    """
    Analyzes the market relevance of a startup idea
    using evidence retrieved from the RAG knowledge base.
    """

    def __init__(self, top_k=5):
        self.top_k = top_k

    def analyze(self, startup_idea):

        if not startup_idea or not startup_idea.strip():
            raise ValueError("Startup idea cannot be empty.")

        # RETRIEVE RAG EVIDENCE
        results = search_startup_ideas(startup_idea, top_k=self.top_k)

        if not results:

            return {
                "startup_idea": startup_idea,
                "primary_market": "Unknown",
                "evidence_count": 0,
                "evidence_strength": "Insufficient",
                "relevant_problems": [],
                "markets_found": [],
                "editions_found": [],
                "evidence": [],
                "message": "No relevant market evidence found.",
            }

        # EXTRACT MARKET INFORMATION
        markets = []
        editions = []
        relevant_problems = []
        evidence = []

        for result in results:
            metadata = result.get("metadata", {})
            market = metadata.get("market", "")
            edition = metadata.get("edition", "")
            problem = metadata.get("problem", "")
            signal_source = metadata.get("signal_source", "")
            source_url = metadata.get("source_url", "")
            distance = result.get("distance", None)

            # -------------------------------------------------
            # UNIQUE MARKETS
            # -------------------------------------------------

            if market and market not in markets:
                markets.append(market)

            # -------------------------------------------------
            # UNIQUE EDITIONS
            # -------------------------------------------------
            if edition and edition not in editions:
                editions.append(edition)

            # -------------------------------------------------
            # PROBLEMS
            # -------------------------------------------------
            if problem:
                relevant_problems.append(problem)

            # -------------------------------------------------
            # SUPPORTING EVIDENCE
            # -------------------------------------------------
            evidence.append(
                {
                    "market": market,
                    "edition": edition,
                    "problem": problem,
                    "signal_source": signal_source,
                    "source_url": source_url,
                    "distance": distance,
                }
            )

        # =====================================================
        # PRIMARY MARKET
        # =====================================================
        market_frequency = {}

        for result in results:

            metadata = result.get("metadata", {})

            market = metadata.get("market", "")

            if market:

                market_frequency[market] = market_frequency.get(market, 0) + 1

        if market_frequency:

            primary_market = max(market_frequency, key=market_frequency.get)

        else:

            primary_market = "Unknown"

        # =====================================================
        # EVIDENCE STRENGTH
        # =====================================================
        evidence_count = len(results)

        if evidence_count >= 5:

            evidence_strength = "Strong"

        elif evidence_count >= 3:

            evidence_strength = "Moderate"

        elif evidence_count >= 1:

            evidence_strength = "Limited"

        else:

            evidence_strength = "Insufficient"

        # =====================================================
        # FINAL RESULT
        # =====================================================
        return {
            "startup_idea": startup_idea,
            "primary_market": primary_market,
            "markets_found": markets,
            "editions_found": editions,
            "evidence_count": evidence_count,
            "evidence_strength": evidence_strength,
            "relevant_problems": relevant_problems,
            "evidence": evidence,
        }


# =============================================================
# CONSOLE DISPLAY
# =============================================================
def display_market_analysis(result):

    print("\n")
    print("=" * 70)
    print("MARKET ANALYSIS AGENT")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nPrimary Market:")
    print(result["primary_market"])

    print("\nMarkets Found:")

    for market in result["markets_found"]:

        print(f"  - {market}")

    print("\nEditions Found:")

    for edition in result["editions_found"]:

        print(f"  - {edition}")

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\nEvidence Strength:")
    print(result["evidence_strength"])

    print("\nRelevant Problems:")

    for index, problem in enumerate(result["relevant_problems"], start=1):

        print(f"\n{index}. {problem}")

    print("\n" + "-" * 70)
    print("Supporting Sources")
    print("-" * 70)

    for index, source in enumerate(result["evidence"], start=1):

        print(f"\nSource {index}")

        print(f"Market        : " f"{source['market']}")

        print(f"Edition       : " f"{source['edition']}")

        print(f"Signal Source : " f"{source['signal_source']}")

        distance = source.get("distance")

        if isinstance(distance, (int, float)):

            print(f"Distance      : " f"{distance:.4f}")

        else:

            print(f"Distance      : " f"{distance}")

        print(f"URL           : " f"{source['source_url']}")

    print("\n" + "=" * 70)


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    test_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    agent = MarketAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_market_analysis(result)
