# YOLO loading & detection

"""
model.py
─────────
YOLOv8 model loading and inference.
Uses st.cache_resource for efficient model reuse.
"""

import time
import cv2
import streamlit as st
from ultralytics import YOLO
from config import (
    COLOR_CORROSION_BGR,
    COLOR_PIPE_BGR,
    COLOR_TEXT_WHITE,
    LABEL_CORROSION,
    LABEL_FONT_SCALE,
    LABEL_THICKNESS,
    BBOX_THICKNESS,
)


@st.cache_resource(show_spinner="Loading YOLOv8n model…")
def load_model(model_path: str) -> YOLO:
    """
    Load YOLO model with Streamlit caching.
    Only loads once per model_path; subsequent calls return cached model.

    Args:
        model_path: Path to .pt weights file

    Returns:
        YOLO model instance
    """
    return YOLO(model_path)


def run_detection(frame_rgb, model: YOLO, conf_thresh: float) -> tuple:
    """
    Run YOLO detection on a single RGB frame.

    Args:
        frame_rgb: numpy array in RGB format (H, W, 3)
        model: Loaded YOLO model
        conf_thresh: Minimum confidence threshold (0.0 - 1.0)

    Returns:
        tuple of:
            - annotated: RGB frame with bounding boxes drawn
            - detections: list of dicts with keys: label, confidence, x1, y1, x2, y2
            - inference_ms: inference time in milliseconds
    """
    t0 = time.perf_counter()
    results = model(frame_rgb, verbose=False, conf=conf_thresh)
    inference_ms = (time.perf_counter() - t0) * 1000

    annotated = frame_rgb.copy()
    detections = []

    for result in results:
        boxes = result.boxes
        if boxes is None:
            continue

        for box in boxes:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            label = result.names[class_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Choose color based on class
            color = COLOR_CORROSION_BGR if label == LABEL_CORROSION else COLOR_PIPE_BGR

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, BBOX_THICKNESS)

            # Draw label background + text
            text = f"{label} {confidence:.2f}"
            (text_w, text_h), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, LABEL_FONT_SCALE, LABEL_THICKNESS
            )
            # Made the background tag slightly larger to fit the bigger text
            cv2.rectangle(
                annotated,
                (x1, y1 - text_h - 8),
                (x1 + text_w + 6, y1),
                color,
                -1,
            )
            cv2.putText(
                annotated,
                text,
                (x1 + 3, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                LABEL_FONT_SCALE,
                COLOR_TEXT_WHITE,
                LABEL_THICKNESS,
            )

            # Store detection info
            detections.append({
                "label": label,
                "confidence": confidence,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
            })

    return annotated, detections, inference_ms


def filter_detections(detections: list, label: str) -> list:
    """
    Filter detections by label.

    Args:
        detections: List of detection dicts
        label: Label to filter by (e.g., "corrosion", "pipe")

    Returns:
        Filtered list of detections
    """
    return [d for d in detections if d["label"] == label]


def get_max_confidence(detections: list, label: str = None) -> float:
    """
    Get maximum confidence from detections, optionally filtered by label.

    Args:
        detections: List of detection dicts
        label: If provided, only consider this label. If None, check all.

    Returns:
        Maximum confidence value, or 0.0 if no matching detections
    """
    if label:
        filtered = filter_detections(detections, label)
    else:
        filtered = detections

    if not filtered:
        return 0.0
    return max(d["confidence"] for d in filtered)


def has_corrosion(detections: list) -> bool:
    """
    Check if any corrosion was detected in the frame.

    Args:
        detections: List of detection dicts

    Returns:
        True if at least one corrosion detection exists
    """
    return any(d["label"] == LABEL_CORROSION for d in detections)