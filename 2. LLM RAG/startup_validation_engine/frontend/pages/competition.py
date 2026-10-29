import streamlit as st

from agents.competitor_agent import CompetitorAgent
from frontend.components.navigation import back_to_dashboard


def show():

    st.title("⚔️ Competition Analysis")

    st.caption("Competitor Agent")

    if not st.session_state.get("startup_idea"):
        st.warning("Please enter a startup idea first.")
        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Competitive Landscape")

    if st.button(
        "⚔️ Run Competition Analysis",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Analyzing competitive evidence..."):

            try:

                agent = CompetitorAgent(top_k=5)

                result = agent.analyze(idea)

                # Stored under "competition_result" so the Dashboard,
                # Validation Score, and Final Report pages (which all
                # read this same key) can see it too.
                st.session_state.competition_result = result

            except Exception as e:

                st.error(f"Competition analysis failed: {str(e)}")

    result = st.session_state.get("competition_result")

    if not result:

        st.info(
            "Click **Run Competition Analysis** "
            "to analyze existing-system and competitor evidence."
        )

        back_to_dashboard()

        return

    # =========================================================
    # COMPETITION INSIGHTS
    # =========================================================

    st.subheader("Competition Insights")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Evidence", result.get("evidence_count", 0))

    with col2:

        markets = result.get("markets_found", [])

        st.metric("Markets Found", len(markets))

    with col3:

        st.metric(
            "Competitor Evidence", result.get("competitor_evidence_status", "Unknown")
        )

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # SPECIFIC COMPETITORS
    # =========================================================

    st.subheader("Specific Competitor Names")

    competitors = result.get("specific_competitors", [])

    if competitors:

        for competitor in competitors:

            st.markdown(f"- **{competitor}**")

    else:

        st.info(
            "No specific competitor names were identified " "from the current dataset."
        )

    # =========================================================
    # SOLUTION / EXISTING-SYSTEM SIGNALS
    # =========================================================

    st.subheader("Solution / Existing-System Signals")

    signals = result.get("solution_signals", [])

    if signals:

        for index, signal in enumerate(signals, start=1):

            with st.expander(f"Signal {index}"):

                st.write(f"**Market:** " f"{signal.get('market', '—')}")

                st.write(f"**Edition:** " f"{signal.get('edition', '—')}")

                detected_terms = signal.get("detected_terms", [])

                if detected_terms:

                    st.write("**Detected Terms:** " + ", ".join(detected_terms))

                st.write(f"**Problem:** " f"{signal.get('problem', '—')}")

                distance = signal.get("distance")

                if isinstance(distance, (int, float)):
                    st.write(f"**Distance:** {distance:.4f}")
                else:
                    st.write("**Distance:** —")

                source_url = signal.get("source_url")

                if source_url:

                    st.markdown(f"[Open Source]({source_url})")

    else:

        st.info("No existing-system signals identified.")

    # =========================================================
    # LIMITATION
    # =========================================================

    # CompetitorAgent explains its limitation under the "message" key.
    limitation = result.get("message")

    if limitation:

        st.markdown(
            "<div class='divider'></div>",
            unsafe_allow_html=True,
        )

        st.subheader("Important Limitation")

        st.warning(limitation)

    # =========================================================
    # NAVIGATION
    # =========================================================

    back_to_dashboard()
