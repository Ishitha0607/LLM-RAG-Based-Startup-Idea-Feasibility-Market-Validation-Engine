import streamlit as st

from frontend.components.cards import score_card
from frontend.components.navigation import next_page
from frontend.pages.home import RESULT_KEYS_TO_RESET

from agents.market_agent import MarketAgent
from agents.customer_pain_agent import CustomerPainAgent
from agents.competitor_agent import CompetitorAgent
from agents.market_gap_agent import MarketGapAgent
from agents.technical_feasibility_agent import TechnicalFeasibilityAgent
from agents.validation_score_agent import ValidationScoreAgent


def run_validation_pipeline(startup_idea):
    """
    Run all startup validation agents and store their
    results in Streamlit session state.
    """

    top_k = 5

    market_agent = MarketAgent(top_k=top_k)
    pain_agent = CustomerPainAgent(top_k=top_k)
    competitor_agent = CompetitorAgent(top_k=top_k)
    gap_agent = MarketGapAgent(top_k=top_k)
    technical_agent = TechnicalFeasibilityAgent(top_k=top_k)
    score_agent = ValidationScoreAgent(top_k=top_k)

    # ---------------------------------------------------------
    # MARKET ANALYSIS
    # ---------------------------------------------------------

    with st.spinner("Analyzing market evidence..."):
        market_result = market_agent.analyze(startup_idea)

    st.session_state.market_result = market_result

    # ---------------------------------------------------------
    # CUSTOMER PAIN ANALYSIS
    # ---------------------------------------------------------

    with st.spinner("Identifying customer pain points..."):
        customer_pain_result = pain_agent.analyze(startup_idea)

    st.session_state.customer_pain_result = customer_pain_result

    # ---------------------------------------------------------
    # COMPETITION ANALYSIS
    # ---------------------------------------------------------

    with st.spinner("Analyzing existing solution signals..."):
        competition_result = competitor_agent.analyze(startup_idea)

    st.session_state.competition_result = competition_result

    # ---------------------------------------------------------
    # MARKET GAP ANALYSIS
    # ---------------------------------------------------------

    with st.spinner("Identifying potential market gaps..."):
        market_gap_result = gap_agent.analyze(startup_idea)

    st.session_state.market_gap_result = market_gap_result

    # ---------------------------------------------------------
    # TECHNICAL FEASIBILITY
    # ---------------------------------------------------------

    with st.spinner("Analyzing technical feasibility..."):
        technical_result = technical_agent.analyze(startup_idea)

    st.session_state.technical_result = technical_result

    # ---------------------------------------------------------
    # VALIDATION SCORE
    # ---------------------------------------------------------

    with st.spinner("Calculating validation score..."):
        validation_score_result = score_agent.analyze(startup_idea)

    st.session_state.validation_score_result = validation_score_result

    st.session_state.analysis_completed = True


def show():

    st.title("📊 Validation Dashboard")

    # =========================================================
    # CHECK STARTUP IDEA
    # =========================================================

    if not st.session_state.get("analysis_started"):

        st.warning("No startup idea has been submitted yet.")

        if st.button("← Go to Startup Input"):

            st.session_state.current_page = "Home"
            st.rerun()

        return

    idea = st.session_state.startup_idea

    # =========================================================
    # STARTUP IDEA
    # =========================================================

    st.caption("CURRENT STARTUP IDEA")

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # RUN VALIDATION
    # =========================================================

    if not st.session_state.get("analysis_completed", False):

        st.subheader("Startup Validation")

        st.write(
            "Run the multi-agent validation pipeline to analyze "
            "your startup idea using the RAG knowledge base."
        )

        if st.button(
            "🚀 Run Validation Analysis",
            type="primary",
            use_container_width=True,
        ):

            try:

                run_validation_pipeline(idea)

                st.success("Startup validation analysis completed successfully.")

                st.rerun()

            except Exception as e:

                st.error(f"Validation analysis failed: {str(e)}")

        return

    # =========================================================
    # VALIDATION RESULTS
    # =========================================================

    score = st.session_state.get("validation_score_result")

    if not score:

        st.warning("Validation score is not available yet.")

        return

    # =========================================================
    # VALIDATION OVERVIEW
    # =========================================================

    st.subheader("Validation Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        score_card(
            "Market Evidence",
            score.get("market_score", 0),
            "Market validation",
        )

    with col2:

        score_card(
            "Customer Pain",
            score.get("customer_pain_score", 0),
            "Problem strength",
        )

    with col3:

        score_card(
            "Competition",
            score.get("competition_score", 0),
            "Competitive opportunity",
        )

    with col4:

        score_card(
            "Market Gap",
            score.get("market_gap_score", 0),
            "Opportunity",
        )

    with col5:

        score_card(
            "Technical",
            score.get("technical_feasibility_score", 0),
            "Feasibility",
        )

    # =========================================================
    # OVERALL SCORE
    # =========================================================

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Overall Validation")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Overall Validation Score", f"{score.get('overall_score', 0)}/100")

    with col2:

        st.metric("Validation Level", score.get("validation_level", "Unknown"))

    # =========================================================
    # EVIDENCE COUNT
    # =========================================================

    st.caption(f"Evidence Records Retrieved: " f"{score.get('evidence_count', 0)}")

    # =========================================================
    # ANALYSIS PIPELINE
    # =========================================================

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Analysis Pipeline")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📈 Analyze Market",
            use_container_width=True,
        ):

            st.session_state.current_page = "Market Analysis"

            st.rerun()

        if st.button(
            "👥 Analyze Customer Pain",
            use_container_width=True,
        ):

            st.session_state.current_page = "Customer Pain"

            st.rerun()

        if st.button(
            "⚔️ Analyze Competition",
            use_container_width=True,
        ):

            st.session_state.current_page = "Competition"

            st.rerun()

    with col2:

        if st.button(
            "🔎 Analyze Market Gap",
            use_container_width=True,
        ):

            st.session_state.current_page = "Market Gap"

            st.rerun()

        if st.button(
            "⚙️ Check Technical Feasibility",
            use_container_width=True,
        ):

            st.session_state.current_page = "Technical Feasibility"

            st.rerun()

        if st.button(
            "🎯 View Validation Score",
            use_container_width=True,
        ):

            st.session_state.current_page = "Validation Score"

            st.rerun()

    # =========================================================
    # FINAL REPORT
    # =========================================================

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Final Analysis")

    if st.button(
        "📄 Generate Final Validation Report",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.current_page = "Final Report"
        st.rerun()

    # =========================================================
    # RESET ANALYSIS
    # =========================================================

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    if st.button(
        "🔄 Start New Startup Validation",
        use_container_width=False,
    ):

        st.session_state.startup_idea = ""
        st.session_state.analysis_started = False
        st.session_state.analysis_completed = False

        for key in RESULT_KEYS_TO_RESET:
            st.session_state[key] = None

        st.session_state.current_page = "Home"

        st.rerun()
