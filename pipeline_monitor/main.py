# only run this later

"""
Pipeline Defect Monitoring System
──────────────────────────────────
YOLOv8n local model · Altair live charts · BlueROV2 RTSP support

Author: Nur Shaheera Husna Mohd Shahril
Universiti Teknologi PETRONAS

Usage:
    streamlit run main.py

    Make sure my_trained_model.pt is in the same directory, or provide the full path
    in the sidebar.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Force the app to look for files in the same folder as main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ── Page configuration (MUST BE FIRST) ───────────────────────────────────────
st.set_page_config(
    page_title="Pipeline Monitor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS Directly Here ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
.top-bar { display: flex; align-items: center; justify-content: space-between; padding: 0.7rem 1.2rem; background: #0D1117; border-radius: 10px; margin-bottom: 1.2rem; border: 1px solid #21262D; }
.top-bar-title { font-size: 15px; font-weight: 600; color: #E6EDF3; letter-spacing: 0.02em; }
.top-bar-sub { font-size: 11px; color: #7D8590; font-family: 'JetBrains Mono', monospace; margin-top: 1px; }
.top-bar-badge { font-size: 11px; font-family: 'JetBrains Mono', monospace; padding: 3px 10px; border-radius: 20px; font-weight: 500; }
.badge-online  { background: #1B3A2A; color: #3FB950; border: 1px solid #238636; }
.badge-offline { background: #2D1B1B; color: #F85149; border: 1px solid #6E3130; }
.badge-idle    { background: #1C2230; color: #79C0FF; border: 1px solid #1F6FEB; }
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.1rem; }
.kpi-card { background: #161B22; border: 1px solid #21262D; border-radius: 10px; padding: 0.85rem 1rem; }
.kpi-label { font-size: 11px; color: #7D8590; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.kpi-value { font-size: 26px; font-weight: 600; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.kpi-sub { font-size: 11px; color: #7D8590; margin-top: 3px; }
.kpi-green { color: #3FB950; }
.kpi-red   { color: #F85149; }
.kpi-blue  { color: #79C0FF; }
.kpi-amber { color: #D29922; }
.status-clear { background: #1B3A2A; border: 1px solid #238636; color: #3FB950; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.status-alert { background: #2D1B1B; border: 1px solid #6E3130; color: #F85149; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 8px; margin-bottom: 8px; animation: pulse 1.2s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(248,81,73,0.3); } 70% { box-shadow: 0 0 0 6px rgba(248,81,73,0); } 100% { box-shadow: 0 0 0 0 rgba(248,81,73,0); } }
.log-entry { font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 3px 0; border-bottom: 1px solid #21262D; color: #7D8590; }
.log-entry.corrosion { color: #F85149; }
.log-entry.clear     { color: #3FB950; }
.section-label { font-size: 11px; color: #7D8590; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-weight: 500; }
[data-testid="stSidebar"] { background: #0D1117; border-right: 1px solid #21262D; }
[data-testid="stSidebar"] label { color: #C9D1D9 !important; font-size: 13px; }
[data-testid="stSidebar"] .stSlider label { color: #7D8590 !important; }
.vega-embed { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True) # <--- THIS IS THE MAGIC LINE

# ── Local modules ──────────────────────────────────────────────────────────────
from config import (
    DEFAULT_MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    FRAME_SKIP,
    AUTO_SAVE_CORROSION,
    DEFAULT_RTSP_URL,
)
# We are NO LONGER calling from styles.py
from state import init_session_state, reset_session_data
from components import render_header, render_kpi_strip, render_section_label, render_log_panel
from tabs.video_tab import render_video_tab
from tabs.live_tab import render_live_tab
from tabs.analytics_tab import render_analytics_tab

# ── Initialize ────────────────────────────────────────────────────────
init_session_state()

# ── Sidebar Panic Button (If it gets lost) ───────────────────────────
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("☰ Menu", help="Force open sidebar"):
        st.sidebar.open()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Model selection
    render_section_label("Model")

    model_path = st.text_input(
        "Weights file",
        value=DEFAULT_MODEL_PATH,
        help="Path to your my_trained_model .pt file. Must be in the same folder as this script, or provide full path.",
    )

    # Detection settings
    render_section_label("Detection settings", margin_top="1rem")
    conf_thresh = st.slider(
        "Confidence threshold",
        min_value=0.10,
        max_value=0.95,
        value=CONFIDENCE_THRESHOLD,
        step=0.05,
    )
    frame_skip = st.slider(
        "Process every Nth frame",
        min_value=1,
        max_value=8,
        value=FRAME_SKIP,
        help="1 = every frame (most accurate). Increase if too slow.",
    )
    save_on_det = st.checkbox(
        "Auto-save frames with corrosion",
        value=AUTO_SAVE_CORROSION,
    )

    # Live stream settings
    render_section_label("Live stream (BlueROV2)", margin_top="1rem")
    rtsp_url = st.text_input(
        "RTSP URL",
        value=DEFAULT_RTSP_URL,
        help="Find in BlueOS → Video Streams",
    )

    # Reset button
    st.markdown("---")
    render_section_label("Controls")
    if st.button("Clear log & counters"):
        reset_session_data()

    # Log panel container
    render_section_label("Detection log")
    log_box = st.container()


# ── Main layout ───────────────────────────────────────────────────────────────
render_header()
render_kpi_strip()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_video, tab_live, tab_analytics = st.tabs([
    "📁  Video file",
    "📡  Live stream",
    "📊  Analytics",
])

with tab_video:
    render_video_tab(
        model_path=model_path,
        conf_thresh=conf_thresh,
        frame_skip=frame_skip,
        save_on_det=save_on_det,
        log_box=log_box,
    )

with tab_live:
    render_live_tab(
        model_path=model_path,
        rtsp_url=rtsp_url,
        conf_thresh=conf_thresh,
        frame_skip=frame_skip,
        save_on_det=save_on_det,
        log_box=log_box,
    )

with tab_analytics:
    render_analytics_tab()