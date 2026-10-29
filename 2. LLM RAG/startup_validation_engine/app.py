"""
Startup Validation Engine — main entry point.

Run with:  streamlit run app.py
"""

import streamlit as st

from frontend.session_state import initialize_session
from frontend.styles import apply_styles
from frontend.components.sidebar import render_sidebar

from frontend.pages import (
    home,
    dashboard,
    market,
    customer_pain,
    competition,
    market_gap,
    technical,
    validation_score,
    final_report,
)


# Maps each sidebar page name to the function that renders it.
PAGE_ROUTES = {
    "Home": home.show,
    "Dashboard": dashboard.show,
    "Market Analysis": market.show,
    "Customer Pain": customer_pain.show,
    "Competition": competition.show,
    "Market Gap": market_gap.show,
    "Technical Feasibility": technical.show,
    "Validation Score": validation_score.show,
    "Final Report": final_report.show,
}


def main():

    st.set_page_config(
        page_title="LLM-RAG Based Startup Idea Feasibility and Market Validation Engine",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    initialize_session()
    apply_styles()
    render_sidebar()

    current_page = st.session_state.get("current_page", "Home")

    if current_page not in PAGE_ROUTES:
        st.session_state.current_page = "Home"
        st.rerun()

    render_current_page = PAGE_ROUTES[current_page]
    render_current_page()


if __name__ == "__main__":
    main()
