# all settings in one place

"""
config.py
─────────
Central configuration for the Pipeline Defect Monitoring System.
All magic numbers and defaults live here for easy tweaking.
"""

# ── Model ──────────────────────────────────────────────────────────────────────
DEFAULT_MODEL_PATH = "my_trained_model.pt"

# ── Detection defaults ─────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.40
FRAME_SKIP = 1
AUTO_SAVE_CORROSION = True

# ── BlueROV2 RTSP ─────────────────────────────────────────────────────────────
DEFAULT_RTSP_URL = "rtsp://192.168.2.2:8554/fpv_stream"

# ── Data buffers (rolling window sizes) ────────────────────────────────────────
CONF_HISTORY_LEN = 120
DETECTION_HISTORY_LEN = 120
FPS_HISTORY_LEN = 60
MAX_LOG_ENTRIES = 25
MAX_SAVED_PREVIEW = 6
CHART_UPDATE_INTERVAL = 10      # update chart every N frames
LIVE_CHART_UPDATE_INTERVAL = 15

# ── Chart display window ──────────────────────────────────────────────────────
CHART_DISPLAY_WINDOW = 80

# ── Colors (BGR for OpenCV, hex for CSS/charts) ───────────────────────────────
COLOR_CORROSION_BGR = (0, 0, 255)       # Pure bright Red
COLOR_PIPE_BGR = (0, 255, 100)           # Neon/Bright Green (highly visible underwater)
BBOX_THICKNESS = 4
LABEL_FONT_SCALE = 1.00
LABEL_THICKNESS = 2
COLOR_CORROSION_HEX = "#0000FF"
COLOR_PIPE_HEX = "#00FF64"
COLOR_BLUE_HEX = "#79C0FF"
COLOR_AMBER_HEX = "#D29922"
COLOR_TEXT_WHITE = (255, 255, 255)

# ── Detection label names ─────────────────────────────────────────────────────
LABEL_CORROSION = "corrosion"
LABEL_PIPE = "pipe"

# ── Supported video formats ────────────────────────────────────────────────────
VIDEO_FORMATS = ["mp4", "avi", "mov"]

# ── Author info (shown in UI header) ──────────────────────────────────────────
AUTHOR_NAME = "Nur Shaheera Husna Mohd Shahril"
UNIVERSITY = "Universiti Teknologi PETRONAS"
PROJECT_YEAR = "2026"