import streamlit as st

from agents.market_gap_agent import MarketGapAgent
from frontend.components.navigation import back_to_dashboard


def show():

    st.title("🔎 Market Gap Analysis")

    st.caption("Market Gap Agent")

    # =========================================================
    # CHECK STARTUP IDEA
    # =========================================================

    if not st.session_state.get("startup_idea"):

        st.warning("Please enter a startup idea first.")

        if st.button("← Go to Startup Input"):

            st.session_state.current_page = "Home"
            st.rerun()

        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Potential Market Gaps")

    # =========================================================
    # RUN MARKET GAP AGENT
    # =========================================================

    if st.button(
        "🔎 Run Market Gap Analysis",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Analyzing unresolved market problems..."):

            try:

                agent = MarketGapAgent(top_k=5)

                result = agent.analyze(idea)

                st.session_state.market_gap_result = result

            except Exception as e:

                st.error(f"Market gap analysis failed: {str(e)}")

    # =========================================================
    # GET RESULT
    # =========================================================

    result = st.session_state.get("market_gap_result")

    if not result:

        st.info(
            "Click **Run Market Gap Analysis** " "to identify potential market gaps."
        )

        back_to_dashboard()

        return

    # =========================================================
    # GAP INSIGHTS
    # =========================================================

    st.subheader("Gap Insights")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Evidence", result.get("evidence_count", 0))

    with col2:

        # MarketGapAgent returns this list under "potential_market_gaps".
        potential_gaps = result.get("potential_market_gaps", [])

        st.metric("Potential Gaps", len(potential_gaps))

    with col3:

        st.metric("Evidence Status", result.get("gap_evidence_status", "Unknown"))

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # UNRESOLVED PROBLEMS
    # =========================================================

    st.subheader("Unresolved Problems")

    problems = result.get("unresolved_problems", [])

    if problems:

        for index, problem in enumerate(problems, start=1):

            with st.expander(f"Problem {index}"):

                st.write(f"**Market:** " f"{problem.get('market', '—')}")

                st.write(f"**Edition:** " f"{problem.get('edition', '—')}")

                st.write(f"**Signal Source:** " f"{problem.get('signal_source', '—')}")

                st.write(f"**Problem:** " f"{problem.get('problem', '—')}")

                distance = problem.get("distance")

                if distance is not None:

                    st.write(f"**Distance:** " f"{distance:.4f}")

                source_url = problem.get("source_url", "")

                if source_url:

                    st.markdown(f"[Open Source]({source_url})")

    else:

        st.info("No unresolved problems identified.")

    # =========================================================
    # POTENTIAL MARKET GAPS
    # =========================================================

    st.subheader("Potential Market Gaps")

    if potential_gaps:

        for index, gap in enumerate(potential_gaps, start=1):

            with st.expander(f"Gap {index}: " f"{gap.get('type', 'Potential Gap')}"):

                st.write(f"**Gap Type:** " f"{gap.get('type', '—')}")

                st.write(f"**Description:** " f"{gap.get('description', '—')}")

                st.write(
                    f"**Supporting Problem:** " f"{gap.get('supporting_problem', '—')}"
                )

                st.write(f"**Market:** " f"{gap.get('market', '—')}")

                st.write(f"**Edition:** " f"{gap.get('edition', '—')}")

                distance = gap.get("distance")

                if distance is not None:

                    st.write(f"**Distance:** " f"{distance:.4f}")

                source_url = gap.get("source_url", "")

                if source_url:

                    st.markdown(f"[Open Source]({source_url})")

    else:

        st.info("No potential market gaps identified.")

    # =========================================================
    # EVIDENCE INTERPRETATION
    # =========================================================

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Evidence Interpretation")

    gap_status = result.get("gap_evidence_status", "Unknown")

    if gap_status == "Strong Evidence of Unresolved Problems":

        st.success(
            "The retrieved evidence contains multiple "
            "signals of unresolved customer problems. "
            "This indicates a potentially meaningful "
            "opportunity, but it does not prove that a "
            "market gap definitely exists."
        )

    elif gap_status == "Moderate Evidence of Unresolved Problems":

        st.info(
            "The retrieved evidence contains several "
            "signals of unresolved problems. Additional "
            "market and customer validation is required."
        )

    elif gap_status == "Limited Evidence":

        st.warning(
            "Only limited evidence of unresolved problems "
            "was identified. Further research is required "
            "before treating the opportunity as a market gap."
        )

    else:

        st.warning(
            "The current evidence is insufficient to "
            "support a meaningful market-gap conclusion."
        )

    # =========================================================
    # RESEARCH LIMITATIONS
    # =========================================================

    # MarketGapAgent returns this list under "research_limitations".
    limitations = result.get("research_limitations", [])

    if limitations:

        st.markdown(
            "<div class='divider'></div>",
            unsafe_allow_html=True,
        )

        st.subheader("Research Limitations")

        for limitation in limitations:

            st.markdown(f"- {limitation}")

    # =========================================================
    # NAVIGATION
    # =========================================================

    back_to_dashboard()
