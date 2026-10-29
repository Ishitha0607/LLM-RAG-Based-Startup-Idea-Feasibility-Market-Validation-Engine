import streamlit as st

from agents.technical_feasibility_agent import TechnicalFeasibilityAgent
from frontend.components.navigation import back_to_dashboard


def show():

    st.title("⚙️ Technical Feasibility")

    st.caption("Technical Feasibility Agent")

    if not st.session_state.get("startup_idea"):
        st.warning("Please enter a startup idea first.")
        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Technical Assessment")

    if st.button(
        "⚙️ Run Technical Feasibility Analysis",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Analyzing technical feasibility..."):

            try:

                agent = TechnicalFeasibilityAgent(top_k=5)

                result = agent.analyze(idea)

                st.session_state.technical_result = result

            except Exception as e:

                st.error(f"Technical feasibility analysis failed: {str(e)}")

    result = st.session_state.get("technical_result")

    if not result:

        st.info(
            "Click **Run Technical Feasibility Analysis** "
            "to perform the technical assessment."
        )

        back_to_dashboard()

        return

    # =========================================================
    # TECHNICAL OVERVIEW
    # =========================================================

    st.subheader("Technical Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Evidence", result.get("evidence_count", 0))

    with col2:

        st.metric("Evidence Strength", result.get("evidence_strength", "—"))

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # FEASIBILITY STATUS
    # =========================================================

    st.subheader("Technical Feasibility Status")

    st.success(result.get("technical_feasibility_status", "Not available"))

    # =========================================================
    # TECHNICAL REQUIREMENTS
    # =========================================================

    st.subheader("Technical Requirements")

    requirements = result.get("technical_requirements", [])

    if requirements:

        for requirement in requirements:

            st.markdown(f"- {requirement}")

    else:

        st.info("No technical requirements identified.")

    # =========================================================
    # TECHNICAL SIGNALS
    # =========================================================

    st.subheader("Technical Signals")

    signals = result.get("technical_signals", [])

    if signals:

        for index, signal in enumerate(signals, start=1):

            with st.expander(f"Signal {index}"):

                st.write(f"**Market:** " f"{signal.get('market', '—')}")

                st.write(f"**Edition:** " f"{signal.get('edition', '—')}")

                detected = signal.get("detected", [])

                if detected:

                    if isinstance(detected, list):

                        st.write("**Detected:** " + ", ".join(detected))

                    else:

                        st.write(f"**Detected:** {detected}")

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

        st.info("No technical signals identified.")

    # =========================================================
    # TECHNICAL RISKS
    # =========================================================

    risks = result.get("technical_risks", [])

    if risks:

        st.markdown(
            "<div class='divider'></div>",
            unsafe_allow_html=True,
        )

        st.subheader("Technical Risks")

        for risk in risks:

            st.warning(risk)

    # =========================================================
    # RESEARCH LIMITATIONS
    # =========================================================

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
