from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from rag.retriever import search_startup_ideas


class ValidationScoreAgent:
    """
    Calculates an evidence-based startup validation score.

    The score considers:
        1. Market Evidence
        2. Customer Pain
        3. Market Gap
        4. Competition Evidence
        5. Technical Feasibility

    This is a preliminary evidence-based score.
    It does not guarantee business success.
    """

    def __init__(self, top_k=5):
        self.top_k = top_k

    # =========================================================
    # MARKET SCORE
    # =========================================================

    def calculate_market_score(self, results):

        if not results:
            return 0

        markets = set()

        for result in results:

            metadata = result.get("metadata", {})

            market = metadata.get("market", "")

            if market:
                markets.add(market)

        evidence_count = len(results)

        score = 0

        # -----------------------------------------------------
        # Evidence Volume
        # -----------------------------------------------------

        if evidence_count >= 5:
            score += 50

        elif evidence_count >= 3:
            score += 35

        elif evidence_count >= 1:
            score += 20

        # -----------------------------------------------------
        # Market Diversity
        # -----------------------------------------------------

        if len(markets) >= 3:
            score += 30

        elif len(markets) == 2:
            score += 20

        elif len(markets) == 1:
            score += 10

        # -----------------------------------------------------
        # Recent Evidence
        # -----------------------------------------------------

        recent_count = 0

        for result in results:

            metadata = result.get("metadata", {})

            edition = metadata.get("edition", "")

            if edition >= "2026-07":
                recent_count += 1

        if recent_count >= 2:
            score += 20

        elif recent_count == 1:
            score += 10

        return min(score, 100)

    # =========================================================
    # CUSTOMER PAIN SCORE
    # =========================================================

    def calculate_customer_pain_score(self, results):

        if not results:
            return 0

        pain_keywords = [
            # Operational pain
            "manual",
            "manually",
            "error",
            "errors",
            "error-prone",
            "problem",
            "problems",
            "limitation",
            "limitations",
            # Difficulty
            "lack",
            "lacks",
            "struggle",
            "struggles",
            "difficult",
            "difficulty",
            "challenge",
            "challenges",
            # Time
            "delay",
            "delays",
            "delayed",
            "time-consuming",
            "tedious",
            "wasting hours",
            "hours",
            # Friction
            "frustrating",
            "frustration",
            "reconcile",
            "reconciling",
            "re-enter",
            "reenter",
            "fragmented",
            # Visibility / integration
            "visibility",
            "real-time",
            "sync",
            "synchronize",
            "synchronization",
            "integration",
            "integrated",
            # Business pain
            "opaque",
            "unpredictable",
            "cannot handle",
            "can't handle",
            "unable",
        ]

        pain_count = 0

        for result in results:

            metadata = result.get("metadata", {})

            problem = metadata.get("problem", "").lower()

            if any(keyword in problem for keyword in pain_keywords):
                pain_count += 1

        ratio = pain_count / len(results)

        # -----------------------------------------------------
        # Strong Customer Pain
        # -----------------------------------------------------

        if ratio >= 0.8:
            return 80

        elif ratio >= 0.6:
            return 70

        elif ratio >= 0.4:
            return 60

        elif ratio > 0:
            return 45

        return 20

    # =========================================================
    # MARKET GAP SCORE
    # =========================================================

    def calculate_gap_score(self, results):

        if not results:
            return 0

        gap_keywords = [
            "poorly integrated",
            "not integrated",
            "lack integration",
            "lack of integration",
            "fragmented",
            "cannot handle",
            "can't handle",
            "unable to",
            "fails to",
            "does not support",
            "doesn't support",
            "missing",
            "limited support",
            "no support",
            "lack",
            "lacks",
        ]

        gap_count = 0

        for result in results:

            metadata = result.get("metadata", {})

            problem = metadata.get("problem", "").lower()

            if any(keyword in problem for keyword in gap_keywords):
                gap_count += 1

        ratio = gap_count / len(results)

        # -----------------------------------------------------
        # IMPORTANT:
        # Repeated pain does NOT prove a market gap.
        # Therefore scores remain conservative.
        # -----------------------------------------------------

        if ratio >= 0.8:
            return 55

        elif ratio >= 0.6:
            return 50

        elif ratio >= 0.4:
            return 45

        elif ratio > 0:
            return 35

        return 20

    # =========================================================
    # COMPETITION SCORE
    # =========================================================

    def calculate_competition_score(self, results):

        if not results:
            return 0

        """
        Competition scoring is intentionally conservative.

        The retrieved dataset primarily contains problem/pain
        signals. A word such as "platform", "system", or
        "software" inside a problem statement is NOT considered
        proof of a competitor.

        Higher score means the competitive opportunity appears
        favorable based on the available evidence.

        However, when no actual competitor evidence exists,
        the score must NOT become 90.
        """

        competitor_keywords = [
            "competitor",
            "competitors",
            "alternative",
            "alternatives",
            "competing",
            "competes with",
            "competes against",
            "market leader",
            "rival",
            "rivals",
            "similar product",
            "similar products",
            "existing solution",
            "existing solutions",
            "existing platform",
            "existing platforms",
            "competitor platform",
        ]

        competitor_count = 0

        for result in results:

            metadata = result.get("metadata", {})

            problem = metadata.get("problem", "").lower()

            market = metadata.get("market", "").lower()

            combined_text = problem + " " + market

            if any(keyword in combined_text for keyword in competitor_keywords):
                competitor_count += 1

        # -----------------------------------------------------
        # No actual competitor evidence
        # -----------------------------------------------------

        if competitor_count == 0:

            # Competitive landscape is unknown.
            # Do not claim that competition is low.
            return 40

        ratio = competitor_count / len(results)

        # -----------------------------------------------------
        # Some competitor evidence
        # -----------------------------------------------------

        if ratio <= 0.2:
            return 70

        elif ratio <= 0.4:
            return 60

        elif ratio <= 0.6:
            return 50

        elif ratio <= 0.8:
            return 40

        return 30

    # =========================================================
    # TECHNICAL FEASIBILITY SCORE
    # =========================================================

    def calculate_technical_score(self, startup_idea, results):

        if not startup_idea:
            return 0

        idea_lower = startup_idea.lower()

        technical_features = [
            "ai",
            "artificial intelligence",
            "machine learning",
            "ml",
            # Forecasting / analytics
            "forecast",
            "forecasting",
            "prediction",
            "predict",
            "analytics",
            "demand",
            # Inventory
            "inventory",
            "stock",
            "warehouse",
            "reorder",
            # Software
            "software",
            "platform",
            "system",
            "application",
            "automation",
            "automatically",
            # Integration
            "integration",
            "integrate",
            "api",
            "apis",
        ]

        detected_features = 0

        for feature in technical_features:

            if feature in idea_lower:
                detected_features += 1

        score = 40

        # -----------------------------------------------------
        # Technical capability signals
        # -----------------------------------------------------

        if detected_features >= 7:
            score += 40

        elif detected_features >= 5:
            score += 30

        elif detected_features >= 3:
            score += 20

        elif detected_features >= 1:
            score += 10

        # -----------------------------------------------------
        # Supporting evidence
        # -----------------------------------------------------

        if len(results) >= 3:
            score += 20

        return min(score, 100)

    # =========================================================
    # OVERALL SCORE
    # =========================================================

    def calculate_overall_score(
        self, market_score, pain_score, gap_score, competition_score, technical_score
    ):

        overall = (
            market_score * 0.25
            + pain_score * 0.25
            + gap_score * 0.20
            + competition_score * 0.10
            + technical_score * 0.20
        )

        return round(overall, 2)

    # =========================================================
    # VALIDATION LEVEL
    # =========================================================

    def determine_validation_level(self, score):

        if score >= 80:

            return "High Validation Potential"

        elif score >= 65:

            return "Good Validation Potential"

        elif score >= 50:

            return "Moderate Validation Potential"

        elif score >= 35:

            return "Low Validation Potential"

        return "Very Low Validation Potential"

    # =========================================================
    # MAIN ANALYSIS
    # =========================================================

    def analyze(
        self,
        startup_idea,
        market_result=None,
        customer_pain_result=None,
        competitor_result=None,
        market_gap_result=None,
        technical_result=None,
    ):

        if not startup_idea or not startup_idea.strip():

            raise ValueError("Startup idea cannot be empty.")

        # -----------------------------------------------------
        # RETRIEVE RAG EVIDENCE
        # -----------------------------------------------------

        results = search_startup_ideas(startup_idea, top_k=self.top_k)

        # -----------------------------------------------------
        # CALCULATE INDIVIDUAL SCORES
        # -----------------------------------------------------

        market_score = self.calculate_market_score(results)

        customer_pain_score = self.calculate_customer_pain_score(results)

        market_gap_score = self.calculate_gap_score(results)

        competition_score = self.calculate_competition_score(results)

        technical_feasibility_score = self.calculate_technical_score(
            startup_idea, results
        )

        # -----------------------------------------------------
        # CALCULATE OVERALL SCORE
        # -----------------------------------------------------

        overall_score = self.calculate_overall_score(
            market_score,
            customer_pain_score,
            market_gap_score,
            competition_score,
            technical_feasibility_score,
        )

        validation_level = self.determine_validation_level(overall_score)

        # -----------------------------------------------------
        # RETURN RESULT
        # -----------------------------------------------------

        return {
            "startup_idea": startup_idea,
            "evidence_count": len(results),
            "market_score": market_score,
            "customer_pain_score": customer_pain_score,
            "market_gap_score": market_gap_score,
            "competition_score": competition_score,
            "technical_feasibility_score": technical_feasibility_score,
            "overall_score": overall_score,
            "validation_level": validation_level,
        }


# =============================================================
# DISPLAY VALIDATION RESULT
# =============================================================


def display_validation_result(result):

    print("\n")
    print("=" * 70)
    print("STARTUP VALIDATION SCORE")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\n" + "-" * 70)
    print("VALIDATION SCORES")
    print("-" * 70)

    print(f"\nMarket Evidence Score" f"       : {result['market_score']}/100")

    print(f"Customer Pain Score" f"         : {result['customer_pain_score']}/100")

    print(f"Market Gap Score" f"            : {result['market_gap_score']}/100")

    print(f"Competition Score" f"           : {result['competition_score']}/100")

    print(
        f"Technical Feasibility Score" f" : {result['technical_feasibility_score']}/100"
    )

    print("\n" + "-" * 70)

    print(f"Overall Validation Score" f"    : {result['overall_score']}/100")

    print(f"Validation Level" f"            : {result['validation_level']}")

    print("\n" + "-" * 70)

    print(
        "Note: This score represents preliminary "
        "evidence-based validation and does not guarantee "
        "startup success."
    )

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

    agent = ValidationScoreAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_validation_result(result)
