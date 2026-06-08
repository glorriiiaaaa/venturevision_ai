"""
app.py
────────────────────────────────────────────────────────────────────────────────
VentureVision AI – Streamlit Application Entry Point

Run with:
    streamlit run app.py
────────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os, sys, subprocess

st.set_page_config(
    page_title="VentureVision AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/venturevision-ai",
        "About": "VentureVision AI – Startup Outcome Prediction & Decision Support",
    },
)

# ── Neumorphic light/dark theme (CSS + sidebar toggle) ────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.theme import apply_theme
apply_theme()

# ── Auto-train model if model.pkl is missing (for Streamlit Cloud) ────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

if not os.path.exists(MODEL_PATH):
    st.info("⏳ First launch: Training ML models... This takes 3-4 minutes. Please wait.")
    progress = st.progress(0, text="Starting training pipeline...")
    progress.progress(10, text="Loading and preprocessing data...")
    result = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "train_model.py")],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    progress.progress(100, text="Done!")
    if result.returncode != 0:
        st.error("❌ Training failed. Error details:")
        st.code(result.stderr[-3000:])
        st.stop()
    else:
        st.success("✅ Model trained! Loading app now...")
        st.rerun()

# ── Global sidebar branding ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="neu-brand">
            <div style="font-size:2.5rem">🚀</div>
            <div style="font-weight:bold;font-size:1.2rem;color:var(--accent)">VentureVision AI</div>
            <div style="font-size:0.8rem;color:var(--muted)">Startup Outcome Prediction</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("**Navigation**")
    st.markdown(
        """
        - 🏠 **Home** – Overview & dataset
        - 🔮 **Predictor** – Get a prediction
        - 💡 **AI Insights** – Strengths & risks
        - 📈 **Analytics** – EDA dashboard
        - 🏆 **Model Performance** – Metrics & ROC
        """
    )
    st.markdown("---")
    st.caption("Built with Streamlit · Scikit-learn · XGBoost · Plotly")

# ── Landing: brief & product overview ─────────────────────────────────────────
st.markdown(
    """
    <div class="neu-hero">
        <h1>🚀 VentureVision AI</h1>
        <p>An AI-powered decision-support system for predicting startup outcomes</p>
        <p>
            <span class="neu-pill">IPO</span>
            <span class="neu-pill">Acquisition</span>
            <span class="neu-pill">Failure Risk</span>
            <span class="neu-pill">Explainable AI</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── In brief ──────────────────────────────────────────────────────────────────
st.subheader("📌 In Brief")
st.markdown(
    """
    **VentureVision AI** helps investors, founders, and analysts answer one hard
    question — *“Where is this startup headed?”* It learns from **100,000+**
    historical startups and predicts whether a company is most likely to **IPO**,
    get **acquired**, or **fail**, then explains *why* with transparent,
    feature-level insights. Instead of relying on gut feeling, you get
    **data-driven probabilities, risk flags, and improvement recommendations** in
    seconds.
    """
)

st.markdown("---")

# ── What you can do (feature cards) ───────────────────────────────────────────
st.subheader("🧭 What You Can Do")
f1, f2, f3 = st.columns(3, gap="large")
features = [
    (f1, "🔮", "Predict Outcomes",
     "Enter a startup's profile — funding, team, traction, market — and get IPO / "
     "Acquisition / Failure probabilities instantly."),
    (f2, "💡", "Understand the Why",
     "Explainable AI surfaces each startup's strengths, risks, and the specific "
     "levers that would most improve its odds."),
    (f3, "📈", "Explore the Data",
     "Interactive dashboards reveal patterns across sectors, funding, revenue, and "
     "burn rate — backed by full model performance metrics."),
]
for col, icon, title, desc in features:
    with col:
        st.markdown(
            f"""
            <div class="neu-card" style="height:200px">
                <div style="font-size:2rem">{icon}</div>
                <div style="font-weight:700;font-size:1.05rem;margin:8px 0;color:var(--accent)">{title}</div>
                <div style="font-size:0.88rem;color:var(--muted)">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── How it works ──────────────────────────────────────────────────────────────
st.subheader("⚙️ How It Works")
s1, s2, s3, s4 = st.columns(4)
steps = [
    (s1, "1", "Input", "Provide a startup's key metrics"),
    (s2, "2", "Model", "Trained ML ensemble scores the profile"),
    (s3, "3", "Predict", "Outcome probabilities are returned"),
    (s4, "4", "Act", "Review insights & recommendations"),
]
for col, num, title, desc in steps:
    with col:
        st.markdown(
            f"""
            <div class="neu-nav">
                <div class="ico" style="color:var(--accent);font-weight:700">{num}</div>
                <div class="t">{title}</div>
                <div class="d">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Key facts + call to action ────────────────────────────────────────────────
st.subheader("📊 At a Glance")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="neu-metric"><h2>100K+</h2><p>Startups Analysed</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="neu-metric"><h2>3</h2><p>Outcome Classes</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="neu-metric"><h2>4</h2><p>ML Models Compared</p></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="neu-metric"><h2>10</h2><p>Input Features</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the sidebar to explore — start with **Home** for details, or jump straight to the **Predictor**.")
