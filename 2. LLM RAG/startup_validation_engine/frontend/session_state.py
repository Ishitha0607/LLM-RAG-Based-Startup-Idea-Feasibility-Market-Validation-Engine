import streamlit as st


def initialize_session():

    defaults = {
        "startup_idea": "",
        "current_page": "Home",
        "analysis_started": False,
        "analysis_completed": False,
        "market_result": None,
        "customer_pain_result": None,
        "competition_result": None,
        "market_gap_result": None,
        "technical_result": None,
        "validation_score_result": None,
        "final_validation_result": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value
