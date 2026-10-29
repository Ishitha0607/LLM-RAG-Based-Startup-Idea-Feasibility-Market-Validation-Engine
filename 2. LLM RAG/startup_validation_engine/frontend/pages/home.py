import streamlit as st

from frontend.components.cards import render_html_block

RESULT_KEYS_TO_RESET = [
    "market_result",
    "customer_pain_result",
    "competition_result",
    "market_gap_result",
    "technical_result",
    "validation_score_result",
    "final_validation_result",
]


def show():

    render_hero_banner()
    render_idea_input_form()
    render_feature_highlights()


def render_hero_banner():
    """Top banner introducing the product (uses the .hero CSS class)."""

    render_html_block(
        """
        <div class="hero">
            <div class="hero-title">
                🚀 LLM-RAG Based Startup Idea Feasibility
                and Market Validation Engine
            </div>
            <div class="hero-description">
                Evaluate startup ideas using evidence-based market analysis,
                customer pain assessment, competition analysis, market-gap
                detection, and technical feasibility evaluation — all
                grounded in real retrieved evidence rather than guesses.
            </div>
        </div>
        """
    )


def render_idea_input_form():
    """Text box + button where the user submits their startup idea."""

    st.subheader("Validate Your Startup Idea")

    idea = st.text_area(
        "Startup Idea",
        value=st.session_state.startup_idea,
        height=180,
        placeholder=(
            "Example: A platform that allows small contractors "
            "to rent construction equipment from nearby businesses "
            "instead of purchasing expensive equipment."
        ),
    )

    if not st.button("🚀 Start Startup Validation", type="primary"):
        return

    if not idea.strip():
        st.error("Please enter a startup idea first.")
        return

    start_new_validation_run(idea.strip())


def start_new_validation_run(idea):
    """Save the idea, clear any previous results, and open the Dashboard."""

    st.session_state.startup_idea = idea
    st.session_state.analysis_started = True
    st.session_state.analysis_completed = False

    for key in RESULT_KEYS_TO_RESET:
        st.session_state[key] = None

    st.session_state.current_page = "Dashboard"
    st.rerun()


def render_feature_highlights():
    """Three-column summary of what the engine does."""

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔍 Evidence-Based")
        st.write(
            "Uses relevant evidence retrieved through "
            "the RAG knowledge base."
        )

    with col2:
        st.subheader("🤖 Multi-Agent Analysis")
        st.write(
            "Analyzes market, customers, competition, "
            "market gaps, and technical feasibility."
        )

    with col3:
        st.subheader("📊 Validation Scoring")
        st.write(
            "Combines the analysis into an overall "
            "startup validation score."
        )
