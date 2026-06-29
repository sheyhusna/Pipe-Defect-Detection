"""
components.py
─────────────
Reusable UI components used across multiple tabs.
Keeps the tab files clean and DRY.
"""

import streamlit as st
from config import (
    AUTHOR_NAME,
    UNIVERSITY,
    PROJECT_YEAR,
    # COLOR_AMBER_HEX,
)


def render_header():
    """Render the top header bar with title and status badge."""
    status_config = {
        "idle":    ("IDLE",    "badge-idle"),
        "running": ("LIVE",    "badge-online"),
        "offline": ("OFFLINE", "badge-offline"),
    }
    status_text, badge_class = status_config.get(
        st.session_state.system_status,
        ("UNKNOWN", "badge-idle"),
    )

    st.markdown(
        f"""
        <div class="top-bar">
          <div>
            <div class="top-bar-title">🔬 Pipeline Defect Monitoring System</div>
            <div class="top-bar-sub">YOLOv8n · BlueROV2 · {UNIVERSITY} FYP {PROJECT_YEAR} · {AUTHOR_NAME}</div>
          </div>
          <span class="top-bar-badge {badge_class}">{status_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_strip():
    """Render the 4-card KPI row below the header."""
    total = st.session_state.total_frames
    corr = st.session_state.corrosion_frames
    rate = f"{corr / total * 100:.1f}%" if total else "—"

    # Calculate FPS from last frame time
    if st.session_state.frame_times:
        last_ms = list(st.session_state.frame_times)[-1]
        fps_val = f"{1000 / last_ms:.1f}" if last_ms > 0 else "—"
    else:
        fps_val = "—"

    st.markdown(
        f"""
        <div class="kpi-row">
          <div class="kpi-card">
            <div class="kpi-label">Frames processed</div>
            <div class="kpi-value kpi-blue">{total:,}</div>
            <div class="kpi-sub">since last reset</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Corrosion detections</div>
            <div class="kpi-value kpi-red">{corr:,}</div>
            <div class="kpi-sub">frames flagged</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Detection rate</div>
            <div class="kpi-value kpi-amber">{rate}</div>
            <div class="kpi-sub">corrosion / total</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Inference speed</div>
            <div class="kpi-value kpi-green">{fps_val}</div>
            <div class="kpi-sub">FPS (last frame)</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_alert(is_corrosion: bool):
    """
    Render a status alert box (corrosion detected / pipeline clear).

    Args:
        is_corrosion: True if corrosion was found in current frame
    """
    if is_corrosion:
        html = '<div class="status-alert">⚠ CORROSION DETECTED</div>'
    else:
        html = '<div class="status-clear">✔ Pipeline clear</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_log_panel():
    """Render the detection log entries in the sidebar."""
    with st.container():
        for entry in st.session_state.log_entries:
            st.markdown(
                f'<div class="log-entry {entry["cls"]}">{entry["text"]}</div>',
                unsafe_allow_html=True,
            )


def render_section_label(text: str, margin_top: str = "0"):
    """
    Render a small uppercase section label.

    Args:
        text: Label text
        margin_top: CSS margin-top value (e.g., "1rem")
    """
    st.markdown(
        f'<div class="section-label" style="margin-top:{margin_top}">{text}</div>',
        unsafe_allow_html=True,
    )