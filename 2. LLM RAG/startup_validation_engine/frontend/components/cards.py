"""
Reusable "card" widgets used across the Streamlit pages.

IMPORTANT: every function here renders through `render_html_block()`
instead of `st.markdown(html, unsafe_allow_html=True)`. Streamlit's
Markdown parser treats any line that starts with 4+ spaces of
indentation as a code block, which silently turns nicely styled
<div> cards into a block of raw HTML text. `render_html_block()`
uses `st.html()` (which does not run Markdown parsing at all) and
falls back to `st.markdown()` only on very old Streamlit versions
that don't have `st.html()` yet.
"""

import streamlit as st


def render_html_block(html):
    """Render raw HTML safely, bypassing Streamlit's Markdown parser."""

    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def _clamp_score(score):
    """Convert any input to a float between 0 and 100."""

    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0

    return max(0.0, min(100.0, value))


def _score_status(score_value):
    """Return the (label, css_class) pair for a 0-100 score."""

    if score_value >= 80:
        return "Excellent", "excellent"
    if score_value >= 60:
        return "Good", "good"
    if score_value >= 40:
        return "Moderate", "moderate"
    return "Low", "low"


def score_card(title, score, description="", icon="📊"):
    """Card showing a 0-100 score with a colored progress bar."""

    score_value = _clamp_score(score)
    status_label, status_class = _score_status(score_value)

    description_html = (
        f'<div class="score-description">{description}</div>'
        if description else ""
    )

    html = (
        f'<div class="score-card">'
        f'<div class="score-card-header">'
        f'<div class="score-icon">{icon}</div>'
        f'<div>'
        f'<div class="score-title">{title}</div>'
        f'<div class="score-status {status_class}">{status_label}</div>'
        f'</div></div>'
        f'<div class="score-value">{score_value:.1f}<span>/100</span></div>'
        f'<div class="score-progress">'
        f'<div class="score-progress-fill {status_class}" style="width:{score_value}%;"></div>'
        f'</div>'
        f'{description_html}'
        f'</div>'
    )

    render_html_block(html)


def metric_card(title, value, subtitle="", icon="📊"):
    """Compact card pairing an icon with a headline number."""

    subtitle_html = (
        f'<div class="metric-card-subtitle">{subtitle}</div>'
        if subtitle else ""
    )

    html = (
        f'<div class="metric-card">'
        f'<div class="metric-card-icon">{icon}</div>'
        f'<div class="metric-card-content">'
        f'<div class="metric-card-title">{title}</div>'
        f'<div class="metric-card-value">{value}</div>'
        f'{subtitle_html}'
        f'</div></div>'
    )

    render_html_block(html)


def analysis_card(title, value, description="", icon="🔍"):
    """Card summarizing a single analysis result (title + big value)."""

    description_html = (
        f'<div class="analysis-card-description">{description}</div>'
        if description else ""
    )

    html = (
        f'<div class="analysis-card">'
        f'<div class="analysis-card-top">'
        f'<div class="analysis-icon">{icon}</div>'
        f'<div class="analysis-card-title">{title}</div>'
        f'</div>'
        f'<div class="analysis-card-value">{value}</div>'
        f'{description_html}'
        f'</div>'
    )

    render_html_block(html)


def _status_css_class(status_text):
    """Map a free-text status word to one of the status-* CSS classes."""

    status_lower = str(status_text).lower()

    if status_lower in ("completed", "success", "ready", "active"):
        return "status-success"
    if status_lower in ("running", "processing", "working"):
        return "status-running"
    if status_lower in ("failed", "error"):
        return "status-error"
    return "status-neutral"


def status_card(title, status, description="", icon="●"):
    """Card showing an agent's or the system's current status."""

    status_class = _status_css_class(status)

    description_html = (
        f'<div class="status-card-description">{description}</div>'
        if description else ""
    )

    html = (
        f'<div class="status-card">'
        f'<div class="status-card-icon">{icon}</div>'
        f'<div class="status-card-content">'
        f'<div class="status-card-title">{title}</div>'
        f'<div class="status-badge {status_class}">{status}</div>'
        f'{description_html}'
        f'</div></div>'
    )

    render_html_block(html)


def agent_card(agent_name, description, status="Ready", icon="🤖",
                button_label="Run Analysis", button_key=None):
    """
    Card describing one validation agent, followed by an action button.

    Returns True on the render where the button was just clicked.
    """

    if button_key is None:
        button_key = agent_name.lower().replace(" ", "_")

    html = (
        f'<div class="agent-card">'
        f'<div class="agent-card-header">'
        f'<div class="agent-card-icon">{icon}</div>'
        f'<div class="agent-card-heading">'
        f'<div class="agent-card-title">{agent_name}</div>'
        f'<div class="agent-card-status">{status}</div>'
        f'</div></div>'
        f'<div class="agent-card-description">{description}</div>'
        f'</div>'
    )

    render_html_block(html)

    return st.button(button_label, key=button_key, use_container_width=True)


def info_card(title, content, icon="💡"):
    """Card for a short informational note or tip."""

    html = (
        f'<div class="info-card">'
        f'<div class="info-card-header">'
        f'<span class="info-card-icon">{icon}</span>'
        f'<span class="info-card-title">{title}</span>'
        f'</div>'
        f'<div class="info-card-content">{content}</div>'
        f'</div>'
    )

    render_html_block(html)


def _priority_css_class(priority_text):
    """Map a free-text priority word to one of the priority-* CSS classes."""

    priority_lower = str(priority_text).lower()

    if priority_lower in ("high", "critical", "strong"):
        return "priority-high"
    if priority_lower in ("medium", "moderate"):
        return "priority-medium"
    return "priority-normal"


def recommendation_card(title, recommendation, priority="Recommended"):
    """Card highlighting a single recommendation with a priority badge."""

    priority_class = _priority_css_class(priority)

    html = (
        f'<div class="recommendation-card">'
        f'<div class="recommendation-header">'
        f'<div class="recommendation-title">{title}</div>'
        f'<div class="recommendation-priority {priority_class}">{priority}</div>'
        f'</div>'
        f'<div class="recommendation-content">{recommendation}</div>'
        f'</div>'
    )

    render_html_block(html)


def section_header(title, subtitle="", icon=""):
    """Consistent section heading used above groups of cards."""

    subtitle_html = (
        f'<div class="section-header-subtitle">{subtitle}</div>'
        if subtitle else ""
    )

    icon_prefix = f"{icon} " if icon else ""

    html = (
        f'<div class="section-header">'
        f'<div class="section-header-title">{icon_prefix}{title}</div>'
        f'{subtitle_html}'
        f'</div>'
    )

    render_html_block(html)
