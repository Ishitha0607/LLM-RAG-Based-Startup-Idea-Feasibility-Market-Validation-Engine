import streamlit as st
import pandas as pd


def validation_score_chart(score_result):
    """
    Display validation scores as a bar chart.

    Expected input:

    {
        "Market Evidence": 75,
        "Customer Pain": 80,
        "Market Gap": 70,
        "Competition": 65,
        "Technical Feasibility": 85
    }
    """

    # =========================================================
    # CHECK INPUT
    # =========================================================

    if not score_result:
        st.info("Validation score data is not available.")
        return

    # =========================================================
    # EXTRACT SCORES
    # =========================================================

    categories = [
        "Market Evidence",
        "Customer Pain",
        "Market Gap",
        "Competition",
        "Technical Feasibility",
    ]

    scores = []

    for category in categories:

        value = score_result.get(category, 0)

        # Safely convert score to number
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0

        # Keep score within valid range
        value = max(0, min(100, value))

        scores.append(value)

    # =========================================================
    # CREATE DATAFRAME
    # =========================================================

    df = pd.DataFrame(
        {
            "Category": categories,
            "Score": scores,
        }
    )

    # =========================================================
    # CHECK WHETHER DATA EXISTS
    # =========================================================

    if df["Score"].sum() == 0:

        st.warning(
            "Validation scores are currently zero. "
            "Please calculate the validation score first."
        )

        return

    # =========================================================
    # DISPLAY SCORE TABLE
    # =========================================================

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # =========================================================
    # BAR CHART
    # =========================================================

    st.bar_chart(
        df,
        x="Category",
        y="Score",
        height=400,
        use_container_width=True,
    )

    # =========================================================
    # EXPLANATION
    # =========================================================

    st.caption(
        "Each score represents the evidence-based strength "
        "of that validation dimension on a 0–100 scale."
    )
