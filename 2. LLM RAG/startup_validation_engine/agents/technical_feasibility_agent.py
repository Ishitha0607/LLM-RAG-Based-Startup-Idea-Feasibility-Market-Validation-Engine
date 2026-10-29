from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from rag.retriever import search_startup_ideas


class TechnicalFeasibilityAgent:
    """
    Performs an initial technical feasibility analysis
    using the startup idea and evidence retrieved from
    the RAG knowledge base.

    The agent identifies technical requirements,
    technical signals, and technical risks.

    It does not claim technical feasibility as proven.
    """

    def __init__(self, top_k=5):
        self.top_k = top_k

    def analyze(self, startup_idea):

        if not startup_idea or not startup_idea.strip():
            raise ValueError("Startup idea cannot be empty.")

        # =====================================================
        # RETRIEVE EVIDENCE
        # =====================================================

        results = search_startup_ideas(startup_idea, top_k=self.top_k)

        # =====================================================
        # IDENTIFY TECHNICAL REQUIREMENTS
        # =====================================================

        idea_lower = startup_idea.lower()

        technical_requirements = []

        if any(
            term in idea_lower
            for term in ["ai", "artificial intelligence", "machine learning", "ml"]
        ):
            technical_requirements.append("Artificial Intelligence / Machine Learning")

        if any(
            term in idea_lower
            for term in ["invoice", "pdf", "document", "extract", "extraction", "ocr"]
        ):
            technical_requirements.append("Document Data Extraction")

        if any(
            term in idea_lower
            for term in [
                "accounting",
                "accounting systems",
                "software",
                "platform",
                "application",
                "api",
                "apis",
            ]
        ):
            technical_requirements.append("Software Integration")

        if any(
            term in idea_lower for term in ["automatically", "automation", "automated"]
        ):
            technical_requirements.append("Workflow Automation")

        if not technical_requirements:
            technical_requirements.append("Application Software Development")

        # Remove duplicates while preserving order
        technical_requirements = list(dict.fromkeys(technical_requirements))

        # =====================================================
        # TECHNICAL SIGNALS AND RISKS
        # =====================================================

        technical_signals = []
        technical_risks = []

        for result in results:

            metadata = result.get("metadata", {})

            problem = metadata.get("problem", "")

            market = metadata.get("market", "")

            edition = metadata.get("edition", "")

            signal_source = metadata.get("signal_source", "")

            source_url = metadata.get("source_url", "")

            distance = result.get("distance", 0)

            problem_lower = problem.lower()

            detected_signals = []

            # -------------------------------------------------
            # SOFTWARE SIGNAL
            # -------------------------------------------------

            if any(
                term in problem_lower
                for term in ["software", "application", "platform", "system"]
            ):
                detected_signals.append("Existing software environment")

            # -------------------------------------------------
            # INTEGRATION SIGNAL
            # -------------------------------------------------

            if any(
                term in problem_lower
                for term in [
                    "integration",
                    "integrated",
                    "sync",
                    "connect",
                    "connected",
                ]
            ):
                detected_signals.append("Integration challenge")

            # -------------------------------------------------
            # AUTOMATION SIGNAL
            # -------------------------------------------------

            if any(
                term in problem_lower
                for term in [
                    "manual",
                    "manually",
                    "re-enter",
                    "data entry",
                    "key in",
                    "reconcile",
                ]
            ):
                detected_signals.append("Automation opportunity")

            # -------------------------------------------------
            # DOCUMENT SIGNAL
            # -------------------------------------------------

            if any(
                term in problem_lower
                for term in ["pdf", "document", "invoice", "unstructured data"]
            ):
                detected_signals.append("Document processing requirement")

            # -------------------------------------------------
            # STORE TECHNICAL SIGNAL
            # -------------------------------------------------

            if detected_signals:

                technical_signals.append(
                    {
                        "problem": problem,
                        "market": market,
                        "edition": edition,
                        "detected": detected_signals,
                        "signal_source": signal_source,
                        "source_url": source_url,
                        "distance": distance,
                    }
                )

            # -------------------------------------------------
            # TECHNICAL RISKS
            # -------------------------------------------------

            if any(
                term in problem_lower
                for term in [
                    "integration",
                    "integrated",
                    "software",
                    "application",
                    "system",
                    "sync",
                ]
            ):

                technical_risks.append(
                    "Integration with existing software "
                    "systems may require additional "
                    "development and testing."
                )

            if any(
                term in problem_lower
                for term in ["pdf", "document", "invoice", "data entry"]
            ):

                technical_risks.append(
                    "Document formats and unstructured data "
                    "may affect extraction reliability."
                )

            if any(
                term in problem_lower
                for term in ["manual", "manually", "re-enter", "reconcile"]
            ):

                technical_risks.append(
                    "Automation workflows may require "
                    "validation and exception handling."
                )

        # Remove duplicate risks
        technical_risks = list(dict.fromkeys(technical_risks))

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
        # FEASIBILITY STATUS
        # =====================================================

        if technical_requirements and technical_signals and evidence_count >= 3:

            technical_feasibility_status = (
                "Technically Plausible - " "Further Validation Required"
            )

        elif technical_requirements:

            technical_feasibility_status = "Potentially Feasible - " "Limited Evidence"

        else:

            technical_feasibility_status = "Insufficient Evidence"

        # =====================================================
        # RESEARCH LIMITATIONS
        # =====================================================

        research_limitations = [
            "The current dataset does not contain detailed technical architecture data.",
            "The retrieved evidence does not prove implementation cost or development time.",
            "Integration complexity cannot be fully determined from the current dataset.",
            "Technical feasibility should be validated with prototype development and API/system testing.",
        ]

        # =====================================================
        # FINAL RESULT
        # =====================================================

        return {
            "startup_idea": startup_idea,
            "technical_requirements": technical_requirements,
            "technical_signals": technical_signals,
            "technical_risks": technical_risks,
            "evidence_count": evidence_count,
            "evidence_strength": evidence_strength,
            "technical_feasibility_status": technical_feasibility_status,
            "research_limitations": research_limitations,
        }


# =============================================================
# DISPLAY FUNCTION
# =============================================================


def display_technical_analysis(result):

    print("\n")
    print("=" * 70)
    print("TECHNICAL FEASIBILITY AGENT")
    print("=" * 70)

    print("\nStartup Idea:")
    print(result["startup_idea"])

    print("\nTechnical Requirements:")

    for requirement in result["technical_requirements"]:
        print(f"  - {requirement}")

    print("\nEvidence Count:")
    print(result["evidence_count"])

    print("\nEvidence Strength:")
    print(result["evidence_strength"])

    print("\nTechnical Feasibility Status:")
    print(result["technical_feasibility_status"])

    print("\nTechnical Signals:")

    if not result["technical_signals"]:

        print("  No technical signals identified.")

    else:

        for index, signal in enumerate(result["technical_signals"], start=1):

            print("\n" + "-" * 70)

            print(f"Signal {index}")

            print(f"Market        : " f"{signal['market']}")

            print(f"Edition       : " f"{signal['edition']}")

            print(f"Detected      : " f"{', '.join(signal['detected'])}")

            print("\nProblem:")
            print(signal["problem"])

            print(f"\nDistance      : " f"{signal['distance']:.4f}")

            print("\nSource URL:")
            print(signal["source_url"])

    print("\n" + "-" * 70)
    print("TECHNICAL RISKS")
    print("-" * 70)

    if not result["technical_risks"]:

        print("\nNo specific technical risks identified.")

    else:

        for risk in result["technical_risks"]:

            print(f"\n- {risk}")

    print("\n" + "-" * 70)
    print("RESEARCH LIMITATIONS")
    print("-" * 70)

    for limitation in result["research_limitations"]:

        print(f"\n- {limitation}")

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

    agent = TechnicalFeasibilityAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_technical_analysis(result)
