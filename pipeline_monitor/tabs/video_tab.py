"""
tabs/video_tab.py
──────────────────
Post-processing approach: Analyzes video offline, updates dashboard, saves images.
"""

import os
import cv2
import tempfile
import time
from datetime import datetime

import streamlit as st

from config import VIDEO_FORMATS
from model import load_model, run_detection, has_corrosion, get_max_confidence
from state import add_saved_frame, add_log_entry


def process_video_offline(video_path, model, conf_thresh, progress_bar, status_text):
    """Runs AI on the video, updates dashboard stats, and saves corrosion images."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        status_text.error("Cannot open video file.")
        return

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        progress_bar.progress(frame_idx / n_frames, text=f"Analyzing frame {frame_idx}/{n_frames}...")
        time.sleep(0.01)  # Lets the progress bar update smoothly

        # Run AI
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        annotated, detections, inference_ms = run_detection(rgb, model, conf_thresh)

        # ── UPDATE DASHBOARD COUNTERS (This fixes the Analytics tab!) ─────────
        st.session_state.total_frames += 1
        if has_corrosion(detections):
            st.session_state.corrosion_frames += 1
        else:
            st.session_state.pipe_frames += 1

        max_corr_conf = get_max_confidence(detections, "corrosion")
        fps_now = 1000 / inference_ms if inference_ms > 0 else 0
        st.session_state.frame_times.append(inference_ms)

        # Update confidence history for charts
        max_pipe_conf = get_max_confidence(detections, "pipe")
        st.session_state.conf_history.append({
            "frame": st.session_state.total_frames,
            "corrosion_conf": round(max_corr_conf, 3),
            "pipe_conf": round(max_pipe_conf, 3),
        })

        # Auto-save high-res images
        if has_corrosion(detections):
            timestamp = datetime.now().strftime("%H%M%S")
            img_path = os.path.join("saved_frames", f"vid_corrosion_f{frame_idx}_{timestamp}.jpg")
            os.makedirs("saved_frames", exist_ok=True)

            # Save with THICK boxes and LARGE text for engineers
            bgr_annotated = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
            cv2.imwrite(img_path, bgr_annotated)
            add_saved_frame(img_path)

        # Log every 20 frames to save CPU
        if frame_idx % 20 == 0 and detections:
            labels_str = ", ".join(f"{d['label']}({d['confidence']:.2f})" for d in detections)
            add_log_entry(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                frame_num=frame_idx,
                source="POST-VID",
                labels_str=labels_str,
                max_conf=max_corr_conf,
                fps_now=fps_now,
                is_corrosion=has_corrosion(detections)
            )

    cap.release()


def render_video_tab(model_path: str, conf_thresh: float, frame_skip: int,
                     save_on_det: bool, log_box):
    """Render the Video File tab content."""

    uploaded = st.file_uploader(
        "Upload ROV footage (.mp4  .avi  .mov)",
        type=VIDEO_FORMATS,
    )

    if not uploaded:
        st.caption("Upload a video file to begin AI analysis.")
        return

    if not os.path.exists(model_path):
        st.error(f"Model not found at `{model_path}`.")
        return

    model = load_model(model_path)

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded.read())
    tfile.flush()

    n_frames = int(cv2.VideoCapture(tfile.name).get(cv2.CAP_PROP_FRAME_COUNT))
    st.caption(f"Loaded — {n_frames:,} frames. Click below to begin offline analysis.")

    if st.button("▶  Process Video (Post-Processing)", type="primary"):
        progress_bar = st.progress(0, text="Starting...")
        status_text = st.empty()

        start_time = time.time()

        process_video_offline(tfile.name, model, conf_thresh, progress_bar, status_text)

        elapsed = time.time() - start_time

        # Clean up temp file safely
        try:
            if os.path.exists(tfile.name):
                os.remove(tfile.name)
        except PermissionError:
            pass

        status_text.success(f"✅ Analysis Complete in {elapsed:.1f}s!")

        # Show a summary instead of a broken video player
        st.markdown(f"""
        <div style="background: #161B22; border:1px solid #21262D; border-radius:10px; padding:1.5rem; margin-top:1rem;">
            <div style="color:#79C0FF; font-size:14px; font-weight:600; margin-bottom:10px;">📥 Post-Processing Summary</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                <div>
                    <div style="color:#7D8590; font-size:12px;">Total Frames Analyzed</div>
                    <div style="color:#E6EDF3; font-size:24px; font-weight:600;">{st.session_state.total_frames:,}</div>
                </div>
                <div>
                    <div style="color:#7D8590; font-size:12px;">Corrosion Frames Saved</div>
                    <div style="color:#F85149; font-size:24px; font-weight:600;">{st.session_state.corrosion_frames:,}</div>
                </div>
            </div>
            <div style="color:#7D8590; font-size:12px; margin-top:15px;">
                ✅ High-resolution images saved to <code style="color:#3FB950">saved_frames/</code> folder.<br>
                ✅ Dashboard & Charts updated. View them in the <b>Analytics</b> tab.
            </div>
        </div>
        """, unsafe_allow_html=True)

        with log_box:
            for entry in st.session_state.log_entries[:15]:
                st.markdown(
                    f'<div class="log-entry {entry["cls"]}">{entry["text"]}</div>',
                    unsafe_allow_html=True,
                )