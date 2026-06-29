# altair charts
"""
charts.py
─────────
Altair chart builders for the analytics dashboard.
All charts use the dark theme matching the app's design.
"""

import pandas as pd
import altair as alt
from config import (
    COLOR_CORROSION_HEX,
    COLOR_PIPE_HEX,
    COLOR_BLUE_HEX,
    # CHART_DISPLAY_WINDOW,
)


def build_confidence_chart(history: list) -> alt.Chart:
    """
    Line chart showing corrosion and pipe confidence over frames.

    Args:
        history: List of dicts with keys: frame, corrosion_conf, pipe_conf

    Returns:
        Altair Chart object
    """
    if not history:
        return alt.Chart(pd.DataFrame()).mark_line()

    df = pd.DataFrame(history)

    base = alt.Chart(df).encode(
        x=alt.X(
            "frame:Q",
            title="Frame",
            axis=alt.Axis(
                labelColor="#7D8590",
                titleColor="#7D8590",
                gridColor="#21262D",
            ),
        )
    )

    corrosion_line = base.mark_line(
        color=COLOR_CORROSION_HEX, strokeWidth=1.5
    ).encode(
        y=alt.Y(
            "corrosion_conf:Q",
            title="Confidence",
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(
                labelColor="#7D8590",
                titleColor="#7D8590",
                gridColor="#21262D",
            ),
        ),
        tooltip=[
            "frame",
            alt.Tooltip("corrosion_conf:Q", format=".2f", title="Corrosion conf"),
        ],
    )

    pipe_line = base.mark_line(
        color=COLOR_PIPE_HEX, strokeWidth=1.5, strokeDash=[4, 2]
    ).encode(
        y=alt.Y("pipe_conf:Q"),
        tooltip=[
            "frame",
            alt.Tooltip("pipe_conf:Q", format=".2f", title="Pipe conf"),
        ],
    )

    chart = (corrosion_line + pipe_line).properties(
        height=160,
        background="transparent",
        title=alt.TitleParams(
            "Detection confidence over time",
            color="#C9D1D9",
            fontSize=12,
        ),
    )

    return chart.configure_view(strokeWidth=0)


def build_fps_chart(fps_history: list) -> alt.Chart:
    """
    Area chart showing inference FPS over frames.

    Args:
        fps_history: List of FPS values (floats)

    Returns:
        Altair Chart object
    """
    if not fps_history:
        return alt.Chart(pd.DataFrame()).mark_area()

    df = pd.DataFrame({
        "frame": range(len(fps_history)),
        "fps": fps_history,
    })

    return (
        alt.Chart(df)
        .mark_area(
            color=COLOR_BLUE_HEX,
            opacity=0.2,
            line={"color": COLOR_BLUE_HEX, "strokeWidth": 1.5},
        )
        .encode(
            x=alt.X(
                "frame:Q",
                title="Frame",
                axis=alt.Axis(
                    labelColor="#7D8590",
                    titleColor="#7D8590",
                    gridColor="#21262D",
                ),
            ),
            y=alt.Y(
                "fps:Q",
                title="FPS",
                scale=alt.Scale(domain=[0, 35]),
                axis=alt.Axis(
                    labelColor="#7D8590",
                    titleColor="#7D8590",
                    gridColor="#21262D",
                ),
            ),
            tooltip=[alt.Tooltip("fps:Q", format=".1f", title="FPS")],
        )
        .properties(
            height=120,
            background="transparent",
            title=alt.TitleParams(
                "Inference speed (FPS)",
                color="#C9D1D9",
                fontSize=12,
            ),
        )
        .configure_view(strokeWidth=0)
    )


def build_class_donut(corrosion_count: int, pipe_count: int) -> alt.Chart:
    """
    Donut chart showing the split between corrosion and pipe detections.

    Args:
        corrosion_count: Number of corrosion frames
        pipe_count: Number of pipe-only frames

    Returns:
        Altair Chart object
    """
    total = corrosion_count + pipe_count
    if total == 0:
        # Avoid division by zero — show empty equal split
        corrosion_count, pipe_count, total = 1, 1, 2

    df = pd.DataFrame({
        "class": ["Corrosion", "Pipe"],
        "count": [corrosion_count, pipe_count],
        "pct": [
            f"{corrosion_count / total * 100:.0f}%",
            f"{pipe_count / total * 100:.0f}%",
        ],
    })

    return (
        alt.Chart(df)
        .mark_arc(innerRadius=38, outerRadius=65)
        .encode(
            theta=alt.Theta("count:Q"),
            color=alt.Color(
                "class:N",
                scale=alt.Scale(
                    domain=["Corrosion", "Pipe"],
                    range=[COLOR_CORROSION_HEX, COLOR_PIPE_HEX],
                ),
                legend=alt.Legend(
                    labelColor="#C9D1D9",
                    titleColor="#7D8590",
                    orient="right",
                    labelFontSize=11,
                ),
            ),
            tooltip=["class", "count", "pct"],
        )
        .properties(
            height=150,
            background="transparent",
            title=alt.TitleParams(
                "Detection class split",
                color="#C9D1D9",
                fontSize=12,
            ),
        )
        .configure_view(strokeWidth=0)
    )