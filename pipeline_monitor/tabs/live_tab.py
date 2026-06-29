"""
tabs/live_tab.py
─────────────────
Reads live_stats.json from the standalone camera script and updates the dashboard.
"""

import os
import json
import time
from datetime import datetime

import streamlit as st
from components import render_section_label

def render_live_tab(model_path, rtsp_url, conf_thresh, frame_skip, save_on_det, log_box):
    """Render the Live Stream Dashboard (Observer Mode)"""

    st.markdown("""
    <div style="background:#161B22; border:1px solid #21262D; border-radius:10px;
                padding:1rem 1.2rem; margin-bottom:1.5rem; font-size:13px; color:#C9D1D9;">
    <b style="color:#79C0FF">📡 Live Mission Control Mode</b><br><br>
    This dashboard is reading live data from the external camera window.<br>
    <span style="color:#D29922"><b>Step 1:</b></span> Run <code style="color:#3FB950">python live_rov_camera.py</code> in your terminal to open the video feed.<br>
    <span style="color:#D29922"><b>Step 2:</b></span> Control the ROV using QGroundControl and your Xbox controller.<br>
    <span style="color:#D29922"><b>Step 3:</b></span> Watch this dashboard update automatically!
    </div>
    """, unsafe_allow_html=True)

    stats_file = "results.json"

    # Try to read the stats file
    if os.path.exists(stats_file):
        try:
            with open(stats_file, "r") as f:
                stats = json.load(f)

            total = stats.get("total_frames", 0)
            corr = stats.get("corrosion_frames", 0)
            fps = stats.get("fps", 0)
            status = stats.get("status", "Waiting...")
            conf = stats.get("max_conf", 0)
            rate = f"{corr/total*100:.1f}%" if total > 0 else "—"

            # Status Alert
            if "CORROSION" in status:
                st.error(f"⚠ {status} | Confidence: {conf:.0%}")
            else:
                st.success(f"✔ {status}")

            # KPI Strip (Matching your main dashboard style)
            st.markdown(f"""
            <div class="kpi-row">
              <div class="kpi-card">
                <div class="kpi-label">Frames processed</div>
                <div class="kpi-value kpi-blue">{total:,}</div>
                <div class="kpi-sub">by external window</div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Corrosion detections</div>
                <div class="kpi-value kpi-red">{corr:,}</div>
                <div class="kpi-sub">frames saved</div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Detection rate</div>
                <div class="kpi-value kpi-amber">{rate}</div>
                <div class="kpi-sub">corrosion / total</div>
              </div>
              <div class="kpi-card">
                <div class="kpi-label">Inference speed</div>
                <div class="kpi-value kpi-green">{fps}</div>
                <div class="kpi-sub">FPS (AI window)</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        except json.JSONDecodeError:
            st.warning("Waiting for camera window to connect...")
    else:
        st.info("⏳ Waiting for `live_rov_camera.py` to start...")
        st.caption("Once you run the Python script, this dashboard will come alive.")

    # Show latest saved frame at the bottom
    render_section_label("Latest Saved Defect Frame", margin_top="1.5rem")
    saved_files = [f for f in os.listdir("saved_frames")] if os.path.exists("saved_frames") else []

    if saved_files:
        # Get the most recently modified file
        latest_file = max(["saved_frames/" + f for f in saved_files], key=os.path.getmtime)
        # FIXED: Changed use_container_width=True to width="stretch"
        st.image(latest_file, caption=os.path.basename(latest_file), width="stretch")
    else:
        st.caption("No corrosion frames saved yet.")