"""
theme.py
────────────────────────────────────────────────────────────────────────────────
Shared neumorphic ("soft UI") theming for VentureVision AI.

Usage (top of every page, right after st.set_page_config):

    from utils.theme import apply_theme
    palette = apply_theme()        # injects CSS + renders the sidebar toggle

`apply_theme()` returns the active palette dict so pages can colour inline
HTML / Plotly traces to match the current light or dark theme.
────────────────────────────────────────────────────────────────────────────────
"""

import copy
import streamlit as st
import plotly.io as pio

# ── Colour palettes ───────────────────────────────────────────────────────────
# Neumorphism uses ONE surface colour with a light shadow (top-left) and a dark
# shadow (bottom-right) to fake soft, extruded plastic. `sd` = shadow-dark,
# `sl` = shadow-light.

LIGHT = {
    "bg":      "#e4e9f2",
    "text":    "#37436b",
    "muted":   "#7a87a8",
    "accent":  "#e8476a",
    "accent2": "#5b73f0",
    "sd":      "#bcc6da",   # dark shadow
    "sl":      "#ffffff",   # light shadow
    "grid":    "rgba(120,134,166,0.20)",
}

DARK = {
    "bg":      "#272a3a",
    "text":    "#c9cee4",
    "muted":   "#8a91ad",
    "accent":  "#ff6384",
    "accent2": "#8aa0ff",
    "sd":      "#1c1e2b",
    "sl":      "#33384d",
    "grid":    "rgba(160,170,200,0.16)",
}

# Semantic outcome colours (work on both themes)
OUTCOME = {"IPO": "#2ecc71", "Acquisition": "#3498db", "Failure": "#e74c3c"}


# ── Static neumorphic CSS (references CSS custom properties) ───────────────────
# Plain (non-f) string → no brace escaping needed. The variables themselves are
# injected separately by `_vars_css()` so the same rules serve both themes.

_STATIC_CSS = """
<style>
/* ── App shell ─────────────────────────────────────────────────────────── */
.stApp { background: var(--bg); color: var(--text); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; }

.stApp, .stMarkdown, p, span, li, label,
[data-testid="stMarkdownContainer"] { color: var(--text); }
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; font-weight: 700; }
a { color: var(--accent2); }
hr { border: none; border-top: 2px solid var(--sd); opacity: .35; }

/* ── Sidebar ───────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg);
    border: none;
    box-shadow: inset -7px 0 14px var(--sd), inset 6px 0 12px var(--sl);
}
[data-testid="stSidebar"] * { color: var(--text); }
[data-testid="stSidebarNav"] a { border-radius: 12px; margin: 2px 8px; }
[data-testid="stSidebarNav"] a:hover {
    background: var(--bg);
    box-shadow: 3px 3px 7px var(--sd), -3px -3px 7px var(--sl);
}

/* ── Buttons ───────────────────────────────────────────────────────────── */
.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--bg);
    color: var(--accent);
    border: none;
    border-radius: 14px;
    padding: 0.55rem 1.3rem;
    font-weight: 600;
    box-shadow: 5px 5px 11px var(--sd), -5px -5px 11px var(--sl);
    transition: all .15s ease;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    color: var(--accent);
    box-shadow: 3px 3px 7px var(--sd), -3px -3px 7px var(--sl);
}
.stButton > button:active,
.stDownloadButton > button:active,
[data-testid="stFormSubmitButton"] > button:active {
    box-shadow: inset 4px 4px 9px var(--sd), inset -4px -4px 9px var(--sl);
}

/* ── Text / number inputs (inset = "pressed in") ───────────────────────── */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 3px 3px 6px var(--sd), inset -3px -3px 6px var(--sl) !important;
}
.stNumberInput button {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: none !important;
}

/* ── Select / multiselect (BaseWeb) ────────────────────────────────────── */
[data-baseweb="select"] > div, [data-baseweb="base-input"] {
    background: var(--bg) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 3px 3px 6px var(--sd), inset -3px -3px 6px var(--sl) !important;
    color: var(--text) !important;
}
[data-baseweb="select"] span, [data-baseweb="select"] svg { color: var(--text) !important; fill: var(--text) !important; }
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="menu"] {
    background: var(--bg) !important;
    border-radius: 12px !important;
    box-shadow: 6px 6px 14px var(--sd), -6px -6px 14px var(--sl) !important;
}
[data-baseweb="menu"] li { background: transparent !important; color: var(--text) !important; }
[data-baseweb="menu"] li:hover {
    background: var(--bg) !important;
    box-shadow: inset 3px 3px 6px var(--sd), inset -3px -3px 6px var(--sl) !important;
}
[data-baseweb="tag"] {
    background: var(--accent) !important;
    color: #fff !important;
    border-radius: 9px !important;
}

/* ── Slider ────────────────────────────────────────────────────────────── */
.stSlider [role="slider"] {
    background: var(--accent) !important;
    box-shadow: 2px 2px 5px var(--sd), -1px -1px 3px var(--sl);
}
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrack"] > div { background: var(--accent) !important; }

/* ── Metric cards ──────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg);
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 6px 6px 13px var(--sd), -6px -6px 13px var(--sl);
}
[data-testid="stMetricValue"] { color: var(--accent); font-weight: 700; }
[data-testid="stMetricLabel"] { color: var(--muted); }

/* ── Expander ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: none !important;
    border-radius: 16px;
    background: var(--bg);
    box-shadow: 5px 5px 11px var(--sd), -5px -5px 11px var(--sl);
    overflow: hidden;
}
[data-testid="stExpander"] summary { color: var(--text); }

/* ── Tabs ──────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: var(--bg);
    border-radius: 12px;
    padding: 6px 16px;
    color: var(--text);
    box-shadow: 4px 4px 9px var(--sd), -4px -4px 9px var(--sl);
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    box-shadow: inset 3px 3px 7px var(--sd), inset -3px -3px 7px var(--sl);
}

/* ── Progress bar ──────────────────────────────────────────────────────── */
.stProgress > div > div { background: var(--bg); box-shadow: inset 2px 2px 5px var(--sd), inset -2px -2px 5px var(--sl); border-radius: 20px; }
.stProgress > div > div > div > div { background: var(--accent) !important; }

/* ── Alerts (keep semantic accent, add soft surface) ───────────────────── */
[data-testid="stAlert"] {
    border-radius: 14px;
    box-shadow: 5px 5px 11px var(--sd), -5px -5px 11px var(--sl);
    border: none;
}

/* ── Dataframe / table ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border-radius: 14px;
    padding: 6px;
    background: var(--bg);
    box-shadow: 5px 5px 11px var(--sd), -5px -5px 11px var(--sl);
}

/* ── Reusable neumorphic components ────────────────────────────────────── */
.neu-hero {
    background: var(--bg);
    border-radius: 26px;
    padding: 42px;
    text-align: center;
    box-shadow: 9px 9px 20px var(--sd), -9px -9px 20px var(--sl);
    margin-bottom: 26px;
}
.neu-hero h1 {
    font-size: 2.9rem; margin: 0 0 10px 0;
    background: linear-gradient(120deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.neu-hero p { color: var(--muted); font-size: 1.1rem; margin: 2px 0; }

.neu-pill {
    display: inline-block;
    background: var(--bg);
    color: var(--accent);
    border-radius: 22px;
    padding: 7px 17px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px;
    box-shadow: 4px 4px 9px var(--sd), -4px -4px 9px var(--sl);
}

.neu-metric {
    background: var(--bg);
    border-radius: 18px;
    padding: 22px 16px;
    text-align: center;
    box-shadow: 6px 6px 13px var(--sd), -6px -6px 13px var(--sl);
}
.neu-metric h2 { color: var(--accent); font-size: 2rem; margin: 0; }
.neu-metric p  { color: var(--muted); margin: 6px 0 0 0; font-size: 0.9rem; }

.neu-card {
    background: var(--bg);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 6px 6px 13px var(--sd), -6px -6px 13px var(--sl);
}

.neu-nav {
    background: var(--bg);
    border-radius: 16px;
    padding: 16px 10px;
    text-align: center;
    height: 122px;
    box-shadow: 5px 5px 11px var(--sd), -5px -5px 11px var(--sl);
    transition: all .15s ease;
}
.neu-nav:hover { box-shadow: inset 4px 4px 9px var(--sd), inset -4px -4px 9px var(--sl); }
.neu-nav .ico { font-size: 1.8rem; }
.neu-nav .t   { font-weight: 700; font-size: 0.92rem; color: var(--text); }
.neu-nav .d   { font-size: 0.74rem; color: var(--muted); margin-top: 4px; }

.prob-card {
    background: var(--bg);
    border-radius: 18px;
    padding: 22px 14px;
    text-align: center;
    box-shadow: 6px 6px 13px var(--sd), -6px -6px 13px var(--sl);
}

.neu-brand {
    text-align: center;
    background: var(--bg);
    border-radius: 20px;
    padding: 18px 10px;
    margin-bottom: 14px;
    box-shadow: 6px 6px 13px var(--sd), -6px -6px 13px var(--sl);
}
</style>
"""


def _vars_css(p: dict) -> str:
    """Inject the active palette as CSS custom properties on :root."""
    return f"""
    <style>
    :root {{
        --bg: {p['bg']};
        --text: {p['text']};
        --muted: {p['muted']};
        --accent: {p['accent']};
        --accent2: {p['accent2']};
        --sd: {p['sd']};
        --sl: {p['sl']};
    }}
    </style>
    """


def _set_plotly_template(p: dict, dark: bool) -> None:
    """Register a Plotly template whose backgrounds match the active theme."""
    base = pio.templates["plotly_dark" if dark else "plotly_white"]
    tmpl = copy.deepcopy(base)
    # Paint chart backgrounds with the theme surface so graphs blend into the UI
    tmpl.layout.paper_bgcolor = p["bg"]
    tmpl.layout.plot_bgcolor = p["bg"]
    tmpl.layout.font.color = p["text"]
    tmpl.layout.title.font.color = p["text"]
    tmpl.layout.xaxis.gridcolor = p["grid"]
    tmpl.layout.yaxis.gridcolor = p["grid"]
    tmpl.layout.xaxis.zerolinecolor = p["grid"]
    tmpl.layout.yaxis.zerolinecolor = p["grid"]
    tmpl.layout.xaxis.linecolor = p["grid"]
    tmpl.layout.yaxis.linecolor = p["grid"]
    tmpl.layout.legend.bgcolor = "rgba(0,0,0,0)"
    pio.templates["venturevision"] = tmpl
    pio.templates.default = "venturevision"


def _patch_plotly_chart() -> None:
    """
    Wrap `st.plotly_chart` so every chart (a) opts out of Streamlit's static
    config theme (`theme=None`) and (b) gets our active template stamped onto
    the figure — needed because `go.Figure` charts don't embed the default
    template the way Plotly Express figures do. Patched once per process.
    """
    if getattr(st, "_vv_plotly_patched", False):
        return
    _orig = st.plotly_chart

    def _themed_plotly_chart(figure_or_data=None, *args, **kwargs):
        kwargs.setdefault("theme", None)
        try:
            if figure_or_data is not None and hasattr(figure_or_data, "update_layout"):
                figure_or_data.update_layout(template="venturevision")
        except Exception:
            pass
        return _orig(figure_or_data, *args, **kwargs)

    st.plotly_chart = _themed_plotly_chart
    st._vv_plotly_patched = True


def apply_theme() -> dict:
    """
    Render the sidebar light/dark toggle, inject the neumorphic CSS, configure
    the Plotly template, and return the active palette dict.
    Call once per page, immediately after `st.set_page_config`.
    """
    # Source of truth lives in a PLAIN (non-widget) key so it survives page
    # navigation — widget-backed keys are not reliably persisted across pages.
    if "theme_dark" not in st.session_state:
        st.session_state["theme_dark"] = False

    # Re-seed the toggle's widget key from the persistent value before the
    # widget is created, so the toggle reflects the right state on every page.
    st.session_state["dark_mode"] = st.session_state["theme_dark"]

    def _sync_theme():
        st.session_state["theme_dark"] = st.session_state["dark_mode"]

    with st.sidebar:
        st.toggle("🌙 Dark mode", key="dark_mode", on_change=_sync_theme,
                  help="Switch between light and dark neumorphic themes")

    dark = st.session_state["theme_dark"]
    palette = DARK if dark else LIGHT

    st.markdown(_vars_css(palette), unsafe_allow_html=True)
    st.markdown(_STATIC_CSS, unsafe_allow_html=True)
    _set_plotly_template(palette, dark)
    _patch_plotly_chart()

    return palette
