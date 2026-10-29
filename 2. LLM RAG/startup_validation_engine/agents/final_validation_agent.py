from pathlib import Path
import sys
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from agents.market_agent import MarketAgent
from agents.customer_pain_agent import CustomerPainAgent
from agents.competitor_agent import CompetitorAgent
from agents.market_gap_agent import MarketGapAgent
from agents.technical_feasibility_agent import TechnicalFeasibilityAgent
from agents.validation_score_agent import ValidationScoreAgent

from dotenv import load_dotenv
import google.generativeai as genai

# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:

    print("WARNING: GOOGLE_API_KEY was not found in .env")

    gemini_model = None

else:

    genai.configure(api_key=GOOGLE_API_KEY)

    gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# =========================================================
# FINAL VALIDATION AGENT
# =========================================================


class FinalValidationAgent:
    """
    Combines the outputs of all startup validation agents
    and generates a final evidence-based validation report
    using Gemini.

    The agent combines:

        1. Market Analysis
        2. Customer Pain Analysis
        3. Competition Analysis
        4. Market Gap Analysis
        5. Technical Feasibility
        6. Validation Score

    The final LLM report is generated only from the
    retrieved evidence and structured agent results.
    """

    def __init__(self, top_k=5):

        self.top_k = top_k

        self.market_agent = MarketAgent(top_k=top_k)

        self.pain_agent = CustomerPainAgent(top_k=top_k)

        self.competitor_agent = CompetitorAgent(top_k=top_k)

        self.gap_agent = MarketGapAgent(top_k=top_k)

        self.technical_agent = TechnicalFeasibilityAgent(top_k=top_k)

        self.score_agent = ValidationScoreAgent(top_k=top_k)

        self.model = gemini_model

    # =====================================================
    # CONVERT RESULT TO JSON
    # =====================================================

    def _format_result(self, result):

        try:

            return json.dumps(result, indent=2, ensure_ascii=False, default=str)

        except Exception:

            return str(result)

    # =====================================================
    # GENERATE FINAL LLM REPORT
    # =====================================================

    def generate_llm_report(
        self,
        startup_idea,
        market_result,
        pain_result,
        competitor_result,
        gap_result,
        technical_result,
        score_result,
    ):

        # -------------------------------------------------
        # GEMINI NOT AVAILABLE
        # -------------------------------------------------

        if not self.model:

            return (
                "Gemini API is not available.\n\n"
                "The structured validation analysis was "
                "completed successfully, but the final "
                "LLM interpretation could not be generated.\n\n"
                "Please verify GOOGLE_API_KEY in the .env file."
            )

        # -------------------------------------------------
        # FORMAT AGENT RESULTS
        # -------------------------------------------------

        market_data = self._format_result(market_result)

        pain_data = self._format_result(pain_result)

        competitor_data = self._format_result(competitor_result)

        gap_data = self._format_result(gap_result)

        technical_data = self._format_result(technical_result)

        score_data = self._format_result(score_result)

        # -------------------------------------------------
        # FINAL PROMPT
        # -------------------------------------------------

        prompt = f"""
        You are an evidence-based startup validation analyst.

        Your task is to prepare a final startup validation report.

        You MUST use ONLY the startup idea and structured
        agent results supplied below.

        Do not invent information.

        Do not add external facts.

        Do not assume information that is not present in
        the supplied evidence.

        ==================================================
        STARTUP IDEA
        ==================================================

        {startup_idea}


        ==================================================
        MARKET ANALYSIS
        ==================================================

        {market_data}


        ==================================================
        CUSTOMER PAIN ANALYSIS
        ==================================================

        {pain_data}


        ==================================================
        COMPETITION ANALYSIS
        ==================================================

        {competitor_data}


        ==================================================
        MARKET GAP ANALYSIS
        ==================================================

        {gap_data}


        ==================================================
        TECHNICAL FEASIBILITY
        ==================================================

        {technical_data}


        ==================================================
        VALIDATION SCORE
        ==================================================

        {score_data}


        ==================================================
        STRICT ANALYSIS RULES
        ==================================================

        Follow these rules carefully:

        1. Do not invent competitor names.

        2. Do not claim that a company is a competitor unless
        the supplied evidence explicitly supports it.

        3. Do not invent market size.

        4. Do not invent customer numbers.

        5. Do not invent revenue figures.

        6. Do not invent investment information.

        7. Do not claim customer willingness to pay.

        8. Do not invent technical capabilities.

        9. Do not claim that a market gap definitely exists.

        10. Treat recurring problems as evidence of an
            unresolved need, not automatic proof of a
            commercial market gap.

        11. Clearly distinguish retrieved evidence from
            interpretation.

        12. Do not treat the validation score as a guarantee
            of startup success.

        13. Mention important evidence limitations.

        14. If evidence is insufficient, clearly state that
            evidence is insufficient.

        15. Do not use information outside the supplied
            agent results.

        ==================================================
        FINAL REPORT FORMAT
        ==================================================

        Prepare the report using exactly the following sections:

        1. Startup Idea Summary

        2. Target Market

        3. Customer Pain Points

        4. Market Evidence

        5. Existing-System and Competitor Evidence

        6. Potential Market Gaps

        7. Technical Feasibility

        8. Key Risks

        9. Validation Score

        10. Evidence-Based Recommendation

        11. Evidence Limitations


        ==================================================
        RECOMMENDATION
        ==================================================

        The Evidence-Based Recommendation section MUST classify
        the startup idea as exactly ONE of these:

        - Strong Potential

        - Promising but Requires Validation

        - Weak Evidence

        - Insufficient Evidence


        Choose the classification based only on the supplied
        evidence and validation results.


        ==================================================
        WRITING REQUIREMENTS
        ==================================================

        Write the report in a professional and concise manner.

        Use clear paragraphs and bullet points where useful.

        Do not exaggerate the findings.

        Do not present assumptions as facts.

        When describing evidence, refer to the retrieved
        problems, markets, editions, signals and sources
        provided by the agents.

        If competitor names are unavailable, explicitly state
        that specific competitor identification is not supported
        by the current dataset.

        If market-size information is unavailable, explicitly
        state that market size cannot be determined from the
        current evidence.

        If willingness-to-pay information is unavailable,
        explicitly state that customer willingness to pay cannot
        be established.

        The final report should provide a balanced assessment
        of the startup idea based on the available RAG evidence.
        """

        # -------------------------------------------------
        # CALL GEMINI
        # -------------------------------------------------

        try:

            response = self.model.generate_content(prompt)

            if response and response.text:

                return response.text.strip()

            return (
                "Gemini returned an empty response. "
                "The structured validation results are "
                "still available."
            )

        except Exception as e:

            return "Gemini report generation failed.\n\n" f"Error: {str(e)}"

    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def analyze(
        self,
        startup_idea,
        market_result=None,
        customer_pain_result=None,
        competitor_result=None,
        market_gap_result=None,
        technical_result=None,
        validation_score_result=None,
    ):
        """
        Combine all six agent results into one final report.

        Each `*_result` argument is optional. If the caller already
        ran that agent earlier in the workflow (e.g. from the
        Dashboard pipeline), pass its result in here so it does not
        need to be recomputed. Any argument left as None is
        calculated automatically.
        """

        if not startup_idea or not startup_idea.strip():

            raise ValueError("Startup idea cannot be empty.")

        # -------------------------------------------------
        # RUN MARKET AGENT (only if not already provided)
        # -------------------------------------------------

        if market_result is None:
            market_result = self.market_agent.analyze(startup_idea)

        # -------------------------------------------------
        # RUN CUSTOMER PAIN AGENT
        # -------------------------------------------------

        if customer_pain_result is None:
            customer_pain_result = self.pain_agent.analyze(startup_idea)

        pain_result = customer_pain_result

        # -------------------------------------------------
        # RUN COMPETITOR AGENT
        # -------------------------------------------------

        if competitor_result is None:
            competitor_result = self.competitor_agent.analyze(startup_idea)

        # -------------------------------------------------
        # RUN MARKET GAP AGENT
        # -------------------------------------------------

        if market_gap_result is None:
            market_gap_result = self.gap_agent.analyze(startup_idea)

        gap_result = market_gap_result

        # -------------------------------------------------
        # RUN TECHNICAL FEASIBILITY AGENT
        # -------------------------------------------------

        if technical_result is None:
            technical_result = self.technical_agent.analyze(startup_idea)

        # -------------------------------------------------
        # RUN VALIDATION SCORE AGENT
        # -------------------------------------------------

        if validation_score_result is None:
            validation_score_result = self.score_agent.analyze(startup_idea)

        score_result = validation_score_result

        # -------------------------------------------------
        # GENERATE FINAL LLM REPORT
        # -------------------------------------------------

        llm_report = self.generate_llm_report(
            startup_idea,
            market_result,
            pain_result,
            competitor_result,
            gap_result,
            technical_result,
            score_result,
        )

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        return {
            "startup_idea": startup_idea,
            "market_analysis": market_result,
            "customer_pain_analysis": pain_result,
            "competitor_analysis": competitor_result,
            "market_gap_analysis": gap_result,
            "technical_feasibility": technical_result,
            "validation_score": score_result,
            "final_llm_report": llm_report,
        }


# =========================================================
# DISPLAY FINAL REPORT
# =========================================================
def display_final_report(result):

    print("\n")

    print("=" * 80)

    print("LLM-RAG STARTUP VALIDATION ENGINE")

    print("=" * 80)

    # -----------------------------------------------------
    # STARTUP IDEA
    # -----------------------------------------------------

    print("\nSTARTUP IDEA")

    print("-" * 80)

    print(result["startup_idea"])

    # -----------------------------------------------------
    # VALIDATION SCORE
    # -----------------------------------------------------

    score = result.get("validation_score", {})

    print("\n")

    print("VALIDATION SCORE")

    print("-" * 80)

    print(f"Market Evidence Score       : " f"{score.get('market_score', 0)}/100")

    print(
        f"Customer Pain Score         : " f"{score.get('customer_pain_score', 0)}/100"
    )

    print(f"Market Gap Score            : " f"{score.get('market_gap_score', 0)}/100")

    print(f"Competition Score           : " f"{score.get('competition_score', 0)}/100")

    print(
        f"Technical Feasibility Score : "
        f"{score.get('technical_feasibility_score', 0)}/100"
    )

    print(f"\nOverall Validation Score    : " f"{score.get('overall_score', 0)}/100")

    print(f"Validation Level            : " f"{score.get('validation_level', '—')}")

    # -----------------------------------------------------
    # FINAL REPORT
    # -----------------------------------------------------

    print("\n")

    print("=" * 80)

    print("FINAL LLM VALIDATION REPORT")

    print("=" * 80)

    print("\n")

    print(result.get("final_llm_report", "No final report available."))

    print("\n")

    print("=" * 80)

    print("VALIDATION COMPLETED")

    print("=" * 80)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    test_idea = (
        "An AI-powered invoice processing platform "
        "for small accounting firms that extracts "
        "data from invoices and automatically updates "
        "accounting systems."
    )

    agent = FinalValidationAgent(top_k=5)

    result = agent.analyze(test_idea)

    display_final_report(result)
