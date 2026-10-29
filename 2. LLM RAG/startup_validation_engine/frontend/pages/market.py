import streamlit as st

from frontend.components.navigation import back_to_dashboard


def show():

    st.title("📈 Market Analysis")

    st.caption("Market Agent")

    # ---------------------------------------------------------
    # CHECK STARTUP IDEA
    # ---------------------------------------------------------

    if not st.session_state.get("startup_idea"):

        st.warning("Please enter a startup idea first.")

        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # CHECK MARKET RESULT
    # ---------------------------------------------------------

    result = st.session_state.get("market_result")

    if not result:

        st.info(
            "Market analysis has not been completed yet. "
            "Please run the validation analysis from the Dashboard."
        )

        back_to_dashboard()

        return

    # ---------------------------------------------------------
    # MARKET EVIDENCE
    # ---------------------------------------------------------

    st.subheader("Market Evidence")

    # ---------------------------------------------------------
    # MARKET INSIGHTS
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Evidence", result.get("evidence_count", 0))

    with col2:

        markets = result.get("markets_found", [])

        st.metric("Markets Found", len(markets))

    with col3:

        st.metric("Evidence Strength", result.get("evidence_strength", "Unknown"))

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # PRIMARY MARKET
    # ---------------------------------------------------------

    st.subheader("Primary Market")

    st.success(result.get("primary_market", "Not identified"))

    # ---------------------------------------------------------
    # MARKETS FOUND
    # ---------------------------------------------------------

    st.subheader("Markets Found")

    if markets:

        for market in markets:

            st.markdown(f"- **{market}**")

    else:

        st.info("No specific markets identified.")

    # ---------------------------------------------------------
    # EDITIONS FOUND
    # ---------------------------------------------------------

    editions = result.get("editions_found", [])

    if editions:

        st.subheader("Evidence Editions")

        for edition in editions:

            st.markdown(f"- **{edition}**")

    # ---------------------------------------------------------
    # RELEVANT PROBLEMS
    # ---------------------------------------------------------

    st.subheader("Relevant Problems")

    problems = result.get("relevant_problems", [])

    if problems:

        for index, problem in enumerate(problems, start=1):

            st.markdown(f"""
                **{index}.** {problem}
                """)

    else:

        st.info("No relevant problems identified.")

    # ---------------------------------------------------------
    # SUPPORTING SOURCES
    # ---------------------------------------------------------

    st.subheader("Supporting Sources")

    # MarketAgent stores its supporting sources under the "evidence" key.
    sources = result.get("evidence", [])

    if sources:

        for index, source in enumerate(sources, start=1):

            with st.expander(f"Source {index}"):

                st.write(f"**Market:** " f"{source.get('market', '—')}")

                st.write(f"**Edition:** " f"{source.get('edition', '—')}")

                st.write(f"**Signal Source:** " f"{source.get('signal_source', '—')}")

                st.write(f"**Problem:** " f"{source.get('problem', '—')}")

                distance = source.get("distance")

                if isinstance(distance, (int, float)):
                    st.write(f"**Distance:** {distance:.4f}")
                else:
                    st.write("**Distance:** —")

                source_url = source.get("source_url", "")

                if source_url:

                    st.markdown(f"[Open Source]({source_url})")

                else:

                    st.caption("No source URL available.")

    else:

        st.info("No supporting sources available.")

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    back_to_dashboard()
