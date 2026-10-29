import streamlit as st

from frontend.components.navigation import back_to_dashboard


def show():

    st.title("👥 Customer Pain Analysis")

    st.caption("Customer Pain Agent")

    # =========================================================
    # CHECK STARTUP IDEA
    # =========================================================

    if not st.session_state.get("startup_idea"):

        st.warning("Please enter a startup idea first.")

        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Customer Pain Points")

    # =========================================================
    # GET STORED RESULT
    # =========================================================

    result = st.session_state.get("customer_pain_result")

    if not result:

        st.info(
            "Customer pain analysis has not been completed yet. "
            "Please run the validation analysis from the Dashboard."
        )

        back_to_dashboard()

        return

    # =========================================================
    # PAIN-POINT INSIGHTS
    # =========================================================

    st.subheader("Pain-Point Insights")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Evidence", result.get("evidence_count", 0))

    with col2:

        categories = result.get("pain_categories", [])

        st.metric("Pain Categories", len(categories))

    with col3:

        st.metric("Evidence Strength", result.get("evidence_strength", "Unknown"))

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # PAIN CATEGORIES
    # =========================================================

    st.subheader("Pain Categories")

    if categories:

        for category in categories:

            st.markdown(f"- **{category}**")

    else:

        st.info("No pain categories identified.")

    # =========================================================
    # IDENTIFIED CUSTOMER PAIN POINTS
    # =========================================================

    st.subheader("Identified Customer Pain Points")

    pain_points = result.get("pain_points", [])

    if pain_points:

        for index, pain in enumerate(pain_points, start=1):

            with st.expander(f"Pain Point {index}"):

                st.write(f"**Category:** " f"{pain.get('category', '—')}")

                st.write(f"**Market:** " f"{pain.get('market', '—')}")

                st.write(f"**Edition:** " f"{pain.get('edition', '—')}")

                st.write("**Problem:**")

                st.write(pain.get("pain_point", "—"))

                st.write(f"**Signal Source:** " f"{pain.get('signal_source', '—')}")

                distance = pain.get("distance")

                if isinstance(distance, (int, float)):

                    st.write(f"**Distance:** " f"{distance:.4f}")

                else:

                    st.write(f"**Distance:** " f"{distance or '—'}")

                source_url = pain.get("source_url", "")

                if source_url:

                    st.markdown(f"[Open Source]({source_url})")

                else:

                    st.caption("No source URL available.")

    else:

        st.info("No customer pain points identified.")

    # =========================================================
    # NAVIGATION
    # =========================================================

    back_to_dashboard()
