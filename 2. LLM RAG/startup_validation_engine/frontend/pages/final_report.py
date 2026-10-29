import streamlit as st
from io import BytesIO
from html import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib import colors

from agents.final_validation_agent import FinalValidationAgent
from frontend.components.navigation import back_to_dashboard

# =========================================================
# PDF GENERATOR
# =========================================================


def create_validation_pdf(
    idea,
    result,
    score,
):
    """
    Generate the final validation report as PDF.
    Raw agent dictionaries are intentionally excluded.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=8,
        textColor=colors.HexColor("#1f2937"),
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=14,
        spaceAfter=18,
        textColor=colors.HexColor("#64748b"),
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=8,
        textColor=colors.HexColor("#111827"),
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7,
        textColor=colors.HexColor("#374151"),
    )

    small_style = ParagraphStyle(
        "ReportSmall",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#6b7280"),
    )

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "Final Validation Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "LLM-RAG Based Startup Idea Feasibility and " "Market Validation Engine",
            subtitle_style,
        )
    )

    # =====================================================
    # STARTUP IDEA
    # =====================================================

    story.append(
        Paragraph(
            "Startup Idea",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            escape(str(idea)),
            body_style,
        )
    )

    # =====================================================
    # VALIDATION SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "Validation Summary",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Score:</b> " f"{score.get('overall_score', 0)}/100",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Validation Level:</b> "
            f"{escape(str(score.get('validation_level', '—')))}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Evidence:</b> " f"{score.get('evidence_count', '—')}",
            body_style,
        )
    )

    # =====================================================
    # VALIDATION DIMENSIONS
    # =====================================================

    story.append(
        Paragraph(
            "Validation Dimensions",
            heading_style,
        )
    )

    dimensions = [
        (
            "Market",
            score.get("market_score", 0),
        ),
        (
            "Customer Pain",
            score.get("customer_pain_score", 0),
        ),
        (
            "Market Gap",
            score.get("market_gap_score", 0),
        ),
        (
            "Competition",
            score.get("competition_score", 0),
        ),
        (
            "Technical Feasibility",
            score.get(
                "technical_feasibility_score",
                0,
            ),
        ),
    ]

    for name, value in dimensions:

        story.append(
            Paragraph(
                f"<b>{escape(name)}:</b> {value}/100",
                body_style,
            )
        )

    # =====================================================
    # FINAL VALIDATION REPORT
    # =====================================================

    story.append(
        Paragraph(
            "Final Validation Report",
            heading_style,
        )
    )

    final_report = result.get(
        "final_llm_report",
        "",
    )

    if final_report:

        clean_report = str(final_report)

        # Remove markdown headings
        clean_report = clean_report.replace(
            "### ",
            "",
        )

        clean_report = clean_report.replace(
            "## ",
            "",
        )

        clean_report = clean_report.replace(
            "# ",
            "",
        )

        # Remove markdown bold
        clean_report = clean_report.replace(
            "**",
            "",
        )

        clean_report = clean_report.replace(
            "__",
            "",
        )

        # Normalize line endings
        clean_report = clean_report.replace(
            "\r\n",
            "\n",
        )

        # Convert markdown bullets
        clean_report = clean_report.replace(
            "\n- ",
            "\n• ",
        )

        clean_report = clean_report.replace(
            "\n* ",
            "\n• ",
        )

        # Normalize excessive blank lines
        while "\n\n\n" in clean_report:

            clean_report = clean_report.replace(
                "\n\n\n",
                "\n\n",
            )

        paragraphs = clean_report.split("\n\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            paragraph = escape(
                paragraph,
                quote=False,
            )

            paragraph = paragraph.replace(
                "\n",
                "<br/>",
            )

            story.append(
                Paragraph(
                    paragraph,
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "Final validation report was not generated.",
                body_style,
            )
        )

    # =====================================================
    # FINAL RECOMMENDATION
    # =====================================================

    recommendation = result.get("recommendation")

    if recommendation:

        story.append(
            Paragraph(
                "Final Recommendation",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                escape(str(recommendation)),
                body_style,
            )
        )

    # =====================================================
    # LIMITATION
    # =====================================================

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "This report represents preliminary "
            "evidence-based validation and does not "
            "guarantee startup success.",
            small_style,
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# PAGE
# =========================================================


def show():

    st.title("📄 Final Validation Report")

    # =====================================================
    # CHECK STARTUP IDEA
    # =====================================================

    if not st.session_state.get("startup_idea"):

        st.warning("Please enter a startup idea first.")

        return

    idea = st.session_state.startup_idea

    st.info(idea)

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # PREVIOUS RESULTS
    # =====================================================

    market_result = st.session_state.get("market_result")

    customer_pain_result = st.session_state.get("customer_pain_result")

    competitor_result = st.session_state.get("competition_result")

    market_gap_result = st.session_state.get("market_gap_result")

    technical_result = st.session_state.get("technical_result")

    validation_score_result = st.session_state.get("validation_score_result")

    # =====================================================
    # REQUIRED RESULTS
    # =====================================================

    missing_results = []

    if not market_result:
        missing_results.append("Market Analysis")

    if not customer_pain_result:
        missing_results.append("Customer Pain")

    if not competitor_result:
        missing_results.append("Competition")

    if not market_gap_result:
        missing_results.append("Market Gap")

    if not technical_result:
        missing_results.append("Technical Feasibility")

    if not validation_score_result:
        missing_results.append("Validation Score")

    if missing_results:

        st.warning(
            "Complete the following analysis stages "
            "before generating the final report:"
        )

        for item in missing_results:

            st.markdown(f"- {item}")

        back_to_dashboard()

        return

    # =====================================================
    # GENERATE FINAL VALIDATION
    # =====================================================

    if st.button(
        "Generate Final Validation Report",
        type="primary",
        use_container_width=False,
    ):

        with st.spinner("Generating final validation report..."):

            try:

                agent = FinalValidationAgent(top_k=5)

                try:

                    result = agent.analyze(
                        idea,
                        market_result=market_result,
                        customer_pain_result=customer_pain_result,
                        competitor_result=competitor_result,
                        market_gap_result=market_gap_result,
                        technical_result=technical_result,
                        validation_score_result=validation_score_result,
                    )

                except TypeError:

                    result = agent.analyze(idea)

                st.session_state.final_validation_result = result

            except Exception as e:

                st.error(f"Final validation failed: {str(e)}")

    # =====================================================
    # GET FINAL RESULT
    # =====================================================

    result = st.session_state.get("final_validation_result")

    if not result:

        st.info(
            "Click **Generate Final Validation Report** "
            "to generate the final report."
        )

        back_to_dashboard()

        return

    # =====================================================
    # SCORE
    # =====================================================

    score = result.get(
        "validation_score",
        validation_score_result,
    )

    if not isinstance(score, dict):

        score = validation_score_result

    # =====================================================
    # VALIDATION SUMMARY
    # =====================================================

    st.subheader("Validation Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Overall Score",
            f"{score.get('overall_score', 0)}/100",
        )

    with col2:

        st.metric(
            "Validation Level",
            score.get(
                "validation_level",
                "—",
            ),
        )

    with col3:

        st.metric(
            "Evidence",
            score.get(
                "evidence_count",
                "—",
            ),
        )

    # =====================================================
    # VALIDATION DIMENSIONS
    # =====================================================

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True,
    )

    st.subheader("Validation Dimensions")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Market",
            f"{score.get('market_score', 0)}/100",
        )

    with col2:

        st.metric(
            "Customer Pain",
            f"{score.get('customer_pain_score', 0)}/100",
        )

    with col3:

        st.metric(
            "Market Gap",
            f"{score.get('market_gap_score', 0)}/100",
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Competition",
            f"{score.get('competition_score', 0)}/100",
        )

    with col2:

        st.metric(
            "Technical Feasibility",
            f"{score.get('technical_feasibility_score', 0)}/100",
        )

    # =====================================================
    # FINAL VALIDATION REPORT
    # =====================================================

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True,
    )

    st.subheader("Final Validation Report")

    final_report = result.get(
        "final_llm_report",
        "",
    )

    if final_report:

        st.markdown(final_report)

        # =================================================
        # DOWNLOAD PDF
        # =================================================

        pdf_data = create_validation_pdf(
            idea=idea,
            result=result,
            score=score,
        )

        st.download_button(
            label="📥 Download PDF",
            data=pdf_data,
            file_name="final_validation_report.pdf",
            mime="application/pdf",
            type="secondary",
        )

    else:

        st.warning("Final validation report was not generated.")

    # =====================================================
    # FINAL RECOMMENDATION
    # =====================================================

    recommendation = result.get("recommendation")

    if recommendation:

        st.markdown(
            '<div class="divider"></div>',
            unsafe_allow_html=True,
        )

        st.subheader("Final Recommendation")

        st.success(recommendation)

    # =====================================================
    # NAVIGATION
    # =====================================================

    back_to_dashboard()
