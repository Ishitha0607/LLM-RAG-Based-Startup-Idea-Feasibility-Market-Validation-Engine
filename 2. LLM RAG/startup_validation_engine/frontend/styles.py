"""
Global styling for the Startup Validation Engine.

This is the ONLY place app-wide CSS lives. Every page and every card
component in frontend/components/cards.py depends on the class names
defined here, so if you add a new card type, add its CSS here too.
"""

import streamlit as st

# Core color palette used across every style rule below.
# This is a fixed LIGHT theme — it does not change based on the visitor's
# OS/browser dark-mode setting, so it looks identical on every system.
# Paired with .streamlit/config.toml (base = "light"), which locks
# Streamlit's own native widgets to the same palette.
COLOR_BACKGROUND = "#f8fafc"
COLOR_SURFACE = "#ffffff"
COLOR_SURFACE_RAISED = "#f1f5f9"
COLOR_BORDER = "#e2e8f0"
COLOR_BORDER_SOFT = "#e8edf3"
COLOR_TEXT_PRIMARY = "#0f172a"
COLOR_TEXT_MUTED = "#475569"
COLOR_ACCENT = "#6366f1"
COLOR_ACCENT_SOFT = "#4f46e5"

COLOR_SUCCESS = "#16a34a"
COLOR_INFO = "#2563eb"
COLOR_WARNING = "#d97706"
COLOR_DANGER = "#dc2626"


def apply_styles():
    """Inject the global stylesheet once per page render."""

    st.markdown(_build_stylesheet(), unsafe_allow_html=True)


def _build_stylesheet():

    return f"""
    <style>

    /* ============================================================
       BASE LAYOUT
    ============================================================ */

    .stApp, .main {{
        background-color: {COLOR_BACKGROUND};
    }}

    .block-container {{
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3 {{
        color: {COLOR_TEXT_PRIMARY} !important;
    }}

    p {{
        color: {COLOR_TEXT_MUTED};
    }}

    .divider {{
        height: 1px;
        background-color: {COLOR_BORDER};
        margin: 1.5rem 0;
        border: none;
    }}

    hr {{
        border-color: {COLOR_BORDER};
    }}

    /* ============================================================
       SIDEBAR
    ============================================================ */

    section[data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid {COLOR_BORDER};
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.5rem;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        border-radius: 0.55rem;
        border: 1px solid {COLOR_BORDER};
        background-color: {COLOR_SURFACE_RAISED};
        color: {COLOR_TEXT_PRIMARY};
        text-align: left;
        font-weight: 600;
        min-height: 2.6rem;
        margin-bottom: 0.25rem;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        border-color: {COLOR_ACCENT};
        background-color: #eef2ff;
        color: {COLOR_ACCENT_SOFT};
    }}

    .sidebar-title {{
        font-size: 1.15rem;
        font-weight: 800;
        color: {COLOR_TEXT_PRIMARY};
        line-height: 1.4;
        margin-bottom: 0.3rem;
    }}

    .sidebar-subtitle {{
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        line-height: 1.4;
    }}

    /* ============================================================
       HERO BANNER (Home page)
    ============================================================ */

    .hero {{
        background: linear-gradient(135deg, #eef2ff, #e0e7ff);
        border: 1px solid #c7d2fe;
        border-radius: 1rem;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }}

    .hero-title {{
        font-size: 2.3rem;
        font-weight: 800;
        color: {COLOR_TEXT_PRIMARY};
        line-height: 1.25;
        margin-bottom: 1rem;
    }}

    .hero-description {{
        font-size: 1rem;
        line-height: 1.7;
        color: {COLOR_TEXT_MUTED};
    }}

    /* ============================================================
       SECTION HEADER
    ============================================================ */

    .section-header {{
        margin-bottom: 0.9rem;
    }}

    .section-header-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .section-header-subtitle {{
        font-size: 0.85rem;
        color: {COLOR_TEXT_MUTED};
        margin-top: 0.15rem;
    }}

    /* ============================================================
       SCORE CARD  (validation scores, 0-100 with progress bar)
    ============================================================ */

    .score-card {{
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.75rem;
        padding: 1rem;
        min-height: 190px;
        box-sizing: border-box;
    }}

    .score-card-header {{
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.8rem;
    }}

    .score-icon {{
        font-size: 1.2rem;
        line-height: 1;
    }}

    .score-title {{
        color: {COLOR_TEXT_PRIMARY};
        font-size: 0.95rem;
        font-weight: 700;
    }}

    .score-status {{
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.15rem;
    }}

    .score-status.excellent {{ color: {COLOR_SUCCESS}; }}
    .score-status.good {{ color: {COLOR_INFO}; }}
    .score-status.moderate {{ color: {COLOR_WARNING}; }}
    .score-status.low {{ color: {COLOR_DANGER}; }}

    .score-value {{
        color: {COLOR_TEXT_PRIMARY};
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.7rem;
    }}

    .score-value span {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.85rem;
        font-weight: 500;
        margin-left: 0.15rem;
    }}

    .score-progress {{
        width: 100%;
        height: 7px;
        background: {COLOR_BORDER};
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 0.8rem;
    }}

    .score-progress-fill {{
        height: 100%;
        border-radius: 999px;
    }}

    .score-progress-fill.excellent {{ background: #22c55e; }}
    .score-progress-fill.good {{ background: #3b82f6; }}
    .score-progress-fill.moderate {{ background: #f59e0b; }}
    .score-progress-fill.low {{ background: #ef4444; }}

    .score-description {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.78rem;
        line-height: 1.4;
    }}

    /* ============================================================
       METRIC CARD  (compact icon + number)
    ============================================================ */

    .metric-card {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.75rem;
        padding: 1rem 1.1rem;
    }}

    .metric-card-icon {{
        font-size: 1.4rem;
        line-height: 1;
    }}

    .metric-card-title {{
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}

    .metric-card-value {{
        font-size: 1.3rem;
        font-weight: 800;
        color: {COLOR_TEXT_PRIMARY};
        line-height: 1.3;
    }}

    .metric-card-subtitle {{
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
    }}

    /* ============================================================
       ANALYSIS CARD (title + big value + description)
    ============================================================ */

    .analysis-card {{
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.75rem;
        padding: 1.1rem;
    }}

    .analysis-card-top {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.6rem;
    }}

    .analysis-icon {{
        font-size: 1.2rem;
    }}

    .analysis-card-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .analysis-card-value {{
        font-size: 1.4rem;
        font-weight: 800;
        color: {COLOR_ACCENT_SOFT};
        margin-bottom: 0.4rem;
    }}

    .analysis-card-description {{
        font-size: 0.8rem;
        color: {COLOR_TEXT_MUTED};
        line-height: 1.4;
    }}

    /* ============================================================
       STATUS CARD (agent / system status pill)
    ============================================================ */

    .status-card {{
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.75rem;
        padding: 1rem;
    }}

    .status-card-icon {{
        font-size: 1.1rem;
        line-height: 1.4;
    }}

    .status-card-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
        margin-bottom: 0.3rem;
    }}

    .status-card-description {{
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        margin-top: 0.3rem;
    }}

    .status-badge {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}

    .status-success {{ background: rgba(74, 222, 128, 0.15); color: {COLOR_SUCCESS}; }}
    .status-running {{ background: rgba(96, 165, 250, 0.15); color: {COLOR_INFO}; }}
    .status-error {{ background: rgba(248, 113, 113, 0.15); color: {COLOR_DANGER}; }}
    .status-neutral {{ background: rgba(148, 163, 184, 0.15); color: {COLOR_TEXT_MUTED}; }}

    /* ============================================================
       AGENT CARD (used above a "Run Analysis" button)
    ============================================================ */

    .agent-card {{
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.75rem;
        padding: 1.1rem;
        margin-bottom: 0.6rem;
    }}

    .agent-card-header {{
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.6rem;
    }}

    .agent-card-icon {{
        font-size: 1.5rem;
    }}

    .agent-card-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .agent-card-status {{
        font-size: 0.75rem;
        color: {COLOR_TEXT_MUTED};
    }}

    .agent-card-description {{
        font-size: 0.82rem;
        color: {COLOR_TEXT_MUTED};
        line-height: 1.45;
    }}

    /* ============================================================
       INFO CARD (tips / explanatory notes)
    ============================================================ */

    .info-card {{
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 0.75rem;
        padding: 1rem 1.1rem;
    }}

    .info-card-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.4rem;
    }}

    .info-card-icon {{
        font-size: 1.05rem;
    }}

    .info-card-title {{
        font-size: 0.88rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .info-card-content {{
        font-size: 0.82rem;
        color: {COLOR_TEXT_MUTED};
        line-height: 1.5;
    }}

    /* ============================================================
       RECOMMENDATION CARD
    ============================================================ */

    .recommendation-card {{
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {COLOR_ACCENT};
        border-radius: 0.6rem;
        padding: 1rem 1.1rem;
        margin-bottom: 0.6rem;
    }}

    .recommendation-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
        gap: 0.6rem;
    }}

    .recommendation-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {COLOR_TEXT_PRIMARY};
    }}

    .recommendation-priority {{
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        white-space: nowrap;
    }}

    .priority-high {{ background: rgba(248, 113, 113, 0.15); color: {COLOR_DANGER}; }}
    .priority-medium {{ background: rgba(251, 191, 36, 0.15); color: {COLOR_WARNING}; }}
    .priority-normal {{ background: rgba(96, 165, 250, 0.15); color: {COLOR_INFO}; }}

    .recommendation-content {{
        font-size: 0.82rem;
        color: {COLOR_TEXT_MUTED};
        line-height: 1.5;
    }}

    /* ============================================================
       STREAMLIT NATIVE WIDGET OVERRIDES
    ============================================================ */

    .stButton > button {{
        border-radius: 0.55rem;
        min-height: 2.7rem;
        font-weight: 600;
    }}

    textarea {{
        background-color: {COLOR_SURFACE} !important;
        color: {COLOR_TEXT_PRIMARY} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 0.6rem !important;
    }}

    input {{
        background-color: {COLOR_SURFACE} !important;
        color: {COLOR_TEXT_PRIMARY} !important;
    }}

    div[data-testid="stMetric"] {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.7rem;
        padding: 1rem;
    }}

    div[data-testid="stExpander"] {{
        background-color: {COLOR_SURFACE_RAISED};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0.6rem;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 0.6rem;
    }}

    /* ============================================================
       SCROLLBAR
    ============================================================ */

    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {COLOR_BACKGROUND}; }}
    ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}

    </style>
    """
