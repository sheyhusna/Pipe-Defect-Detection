# session state logic

"""
state.py
─────────
Manages all Streamlit session_state variables.
Call init_session_state() once at the top of main.py.
"""

from collections import deque
import streamlit as st
from config import (
    CONF_HISTORY_LEN,
    DETECTION_HISTORY_LEN,
    FPS_HISTORY_LEN,
)


def init_session_state():
    """
    Initialize default session state values if they don't exist yet.
    Safe to call multiple times — only sets missing keys.
    """

    defaults = {
        # Counters
        "total_frames":     0,
        "corrosion_frames": 0,
        "pipe_frames":      0,

        # Rolling data buffers
        "conf_history":      deque(maxlen=CONF_HISTORY_LEN),
        "detection_history": deque(maxlen=DETECTION_HISTORY_LEN),
        "frame_times":       deque(maxlen=FPS_HISTORY_LEN),

        # Logs & saved frames
        "log_entries":  [],
        "saved_frames": [],

        # System status: "idle" | "running" | "offline"
        "system_status": "idle",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def reset_session_data():
    """
    Clear all runtime data (counters, logs, buffers).
    Called when user clicks "Clear log & counters".
    Does NOT reset system_status.
    """
    st.session_state.total_frames = 0
    st.session_state.corrosion_frames = 0
    st.session_state.pipe_frames = 0
    st.session_state.conf_history.clear()
    st.session_state.detection_history.clear()
    st.session_state.frame_times.clear()
    st.session_state.log_entries = []
    # Note: saved_frames list is NOT cleared — those are actual files on disk


def add_log_entry(timestamp: str, frame_num: int, source: str, labels_str: str, max_conf: float, fps_now: float,
                  is_corrosion: bool):
    """
    Add a structured log entry.
    """
    display_text = f"[{timestamp}] {source} f{frame_num}: {labels_str}  {fps_now:.1f}fps"
    cls = "corrosion" if is_corrosion else "clear"

    st.session_state.log_entries.insert(0, {
        "text": display_text,
        "cls": cls,
        "timestamp": timestamp,
        "frame": frame_num,
        "source": source,
        "labels": labels_str,
        "max_conf": max_conf,
        "fps": fps_now,
        "is_corrosion": is_corrosion
    })

    # Keep log size bounded
    from config import MAX_LOG_ENTRIES
    if len(st.session_state.log_entries) > MAX_LOG_ENTRIES:
        st.session_state.log_entries = st.session_state.log_entries[:MAX_LOG_ENTRIES]


def add_saved_frame(filepath: str):
    """
    Track a saved frame file.

    Args:
        filepath: Path to the saved .jpg file
    """
    if filepath not in st.session_state.saved_frames:
        st.session_state.saved_frames.append(filepath)