"""
live_rov_camera.py
───────────────────
High-speed camera window. Writes stats to live_stats.json for the dashboard.
"""

import cv2
import time
import os
import json
from datetime import datetime
from ultralytics import YOLO

# ── Settings ──────────────────────────────────────────────────────────────
# USE YOUR EXACT URL HERE:
RTSP_URL = "rtsp://192.168.2.2:8554/video_rtsp_stream_0"
MODEL_PATH = "my_trained_model.pt"
CONFIDENCE = 0.40
FRAME_SKIP = 2
SAVE_DIR = "saved_frames"
STATS_FILE = "live_stats.json"

# ── Setup ─────────────────────────────────────────────────────────────────
os.makedirs(SAVE_DIR, exist_ok=True)
print("Loading AI Model...")
model = YOLO(MODEL_PATH)
print("Connecting to BlueROV2...")

# Force FFmpeg and reduce buffer for BlueROV2 (Prevents timeout)
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("ERROR: Cannot connect to ROV.")
    print("Check: 1) Is the ROV powered on? 2) Is the ethernet cable plugged in? 3) Is your laptop IP 192.168.2.1?")
    input("Press Enter to exit...")
    exit()

print("SUCCESS! Video window is open. Press 'Q' to quit.")

frame_idx = 0
corrosion_count = 0
total_processed = 0

# ── High-Speed Loop ───────────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.1)
        cap = cv2.VideoCapture(RTSP_URL)
        continue

    frame_idx += 1
    if frame_idx % FRAME_SKIP != 0:
        cv2.imshow("BlueROV2 AI Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        continue

    # ── Run AI ────────────────────────────────────────────────────────────
    t0 = time.time()
    results = model(frame, verbose=False, conf=CONFIDENCE)
    inference_ms = (time.time() - t0) * 1000
    fps = 1000 / inference_ms if inference_ms > 0 else 0

    annotated = frame.copy()
    corrosion_found = False
    max_conf = 0.0

    for r in results:
        for box in (r.boxes or []):
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = r.names[cls]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            color = (0, 0, 255) if label == "corrosion" else (0, 255, 100)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
            txt = f"{label} {conf:.2f}"
            cv2.putText(annotated, txt, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            if label == "corrosion":
                corrosion_found = True
                if conf > max_conf: max_conf = conf

    total_processed += 1

    # ── Save Corrosion ────────────────────────────────────────────────────
    if corrosion_found:
        corrosion_count += 1
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"live_corrosion_f{frame_idx}_{timestamp}.jpg"
        cv2.imwrite(os.path.join(SAVE_DIR, filename), annotated)
        cv2.putText(annotated, "ALERT: SAVED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        status_text = "CORROSION DETECTED"
    else:
        cv2.putText(annotated, "CLEAR", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        status_text = "Pipeline Clear"

    # ── Write stats for Streamlit (Do this every 5 frames to save CPU) ───
    if total_processed % 5 == 0:
        stats = {
            "total_frames": total_processed,
            "corrosion_frames": corrosion_count,
            "fps": round(fps, 1),
            "status": status_text,
            "max_conf": round(max_conf, 2)
        }
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)

    # ── Show Window ───────────────────────────────────────────────────────
    cv2.imshow("BlueROV2 AI Feed", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
os.remove(STATS_FILE)  # Clean up file when closed
print(f"Session ended. Saved {corrosion_count} frames.")