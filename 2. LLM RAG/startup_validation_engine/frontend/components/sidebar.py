import streamlit as st

# =========================================================
# SIDEBAR
# =========================================================


def render_sidebar():
    """
    Render application sidebar and manage navigation.
    """

    # =========================================================
    # INITIALIZE CURRENT PAGE
    # =========================================================

    if "current_page" not in st.session_state:

        st.session_state.current_page = "Home"

    # =========================================================
    # NAVIGATION PAGES
    # =========================================================

    pages = [
        ("🏠", "Home"),
        ("📊", "Dashboard"),
        ("📈", "Market Analysis"),
        ("👥", "Customer Pain"),
        ("⚔️", "Competition"),
        ("🔎", "Market Gap"),
        ("⚙️", "Technical Feasibility"),
        ("🎯", "Validation Score"),
        ("📄", "Final Report"),
    ]

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:

        # =====================================================
        # PROJECT BRAND
        # =====================================================

        st.markdown("🚀 **LLM-RAG Startup Validation**")

        st.caption("Feasibility & Market Validation Engine")

        st.divider()

        # =====================================================
        # SECTION
        # =====================================================

        st.caption("ANALYSIS")

        # =====================================================
        # NAVIGATION
        # =====================================================

        for icon, page_name in pages:

            # -------------------------------------------------
            # CHECK ACTIVE PAGE
            # -------------------------------------------------

            is_active = st.session_state.current_page == page_name

            # -------------------------------------------------
            # ACTIVE PAGE
            # -------------------------------------------------

            if is_active:

                st.success(f"{icon}  {page_name}")

            # -------------------------------------------------
            # INACTIVE PAGE
            # -------------------------------------------------

            else:

                if st.button(
                    f"{icon}  {page_name}",
                    key=f"sidebar_{page_name}",
                    use_container_width=True,
                ):

                    st.session_state.current_page = page_name

                    st.rerun()

        # =====================================================
        # SYSTEM STATUS
        # =====================================================

        st.divider()

        st.caption("SYSTEM")

        st.success("● Engine Ready")

        st.caption("LLM + RAG Multi-Agent System")
