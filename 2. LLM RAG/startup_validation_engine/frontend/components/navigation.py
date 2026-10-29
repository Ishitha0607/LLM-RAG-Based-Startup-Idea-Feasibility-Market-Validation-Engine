import streamlit as st

# ============================================================
# PAGE ORDER
# ============================================================

PAGE_ORDER = [
    "Home",
    "Dashboard",
    "Market Analysis",
    "Customer Pain",
    "Competition",
    "Market Gap",
    "Technical Feasibility",
    "Validation Score",
    "Final Report",
]


# ============================================================
# INITIALIZE NAVIGATION
# ============================================================


def initialize_navigation():

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    if "startup_idea" not in st.session_state:
        st.session_state.startup_idea = ""

    if "analysis_started" not in st.session_state:
        st.session_state.analysis_started = False


# ============================================================
# GET CURRENT PAGE INDEX
# ============================================================


def get_current_page_index():

    current_page = st.session_state.get("current_page", "Home")

    if current_page in PAGE_ORDER:
        return PAGE_ORDER.index(current_page)

    return 0


# ============================================================
# GO TO PAGE
# ============================================================


def go_to_page(page_name):

    if page_name in PAGE_ORDER:

        st.session_state.current_page = page_name
        st.rerun()


# ============================================================
# NEXT PAGE
# ============================================================


def next_page():

    current_index = get_current_page_index()

    if current_index < len(PAGE_ORDER) - 1:

        st.session_state.current_page = PAGE_ORDER[current_index + 1]

        st.rerun()


# ============================================================
# PREVIOUS PAGE
# ============================================================


def previous_page():

    current_index = get_current_page_index()

    if current_index > 0:

        st.session_state.current_page = PAGE_ORDER[current_index - 1]

        st.rerun()


# ============================================================
# BACK TO DASHBOARD
# ============================================================


def back_to_dashboard():

    if st.button("← Back to Dashboard", use_container_width=True):

        st.session_state.current_page = "Dashboard"
        st.rerun()


# ============================================================
# NAVIGATION FOOTER
# ============================================================


def render_navigation():

    current_index = get_current_page_index()

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:

        if current_index > 0:

            if st.button("← Back", key="navigation_back", use_container_width=True):

                previous_page()

    with col2:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding-top:0.7rem;
                color:#64748b;
                font-size:0.82rem;
            ">
                Step {current_index + 1}
                of
                {len(PAGE_ORDER)}
                <br>
                <span style="
                    color:#0f172a;
                    font-weight:600;
                ">
                    {PAGE_ORDER[current_index]}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        if current_index < len(PAGE_ORDER) - 1:

            if st.button("Next →", key="navigation_next", use_container_width=True):

                next_page()


# ============================================================
# ANALYSIS WORKFLOW NAVIGATION
# ============================================================


def render_analysis_navigation():

    analysis_pages = [
        "Market Analysis",
        "Customer Pain",
        "Competition",
        "Market Gap",
        "Technical Feasibility",
        "Validation Score",
        "Final Report",
    ]

    current_page = st.session_state.get("current_page", "Home")

    if current_page not in analysis_pages:
        return

    current_index = analysis_pages.index(current_page)

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:

        if current_index > 0:

            if st.button(
                "← Previous",
                key=f"analysis_previous_{current_page}",
                use_container_width=True,
            ):

                st.session_state.current_page = analysis_pages[current_index - 1]

                st.rerun()

    with col2:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding-top:0.6rem;
                color:#7f8b9a;
                font-size:0.8rem;
            ">
                Analysis Stage
                <br>
                <span style="
                    color:#f1f5f9;
                    font-size:0.9rem;
                    font-weight:650;
                ">
                    {current_index + 1}
                    /
                    {len(analysis_pages)}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        if current_index < len(analysis_pages) - 1:

            if st.button(
                "Continue →",
                key=f"analysis_next_{current_page}",
                use_container_width=True,
            ):

                st.session_state.current_page = analysis_pages[current_index + 1]

                st.rerun()
