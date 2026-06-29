# all CSS in one place

"""
styles.py
─────────
All CSS styling for the Streamlit application.
Injected once via st.markdown() in main.py.
"""

CSS = """
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem; padding-bottom: 1rem; }

/* ── Top header bar ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.7rem 1.2rem;
    background: #0D1117;
    border-radius: 10px;
    margin-bottom: 1.2rem;
    border: 1px solid #21262D;
}
.top-bar-title {
    font-size: 15px;
    font-weight: 600;
    color: #E6EDF3;
    letter-spacing: 0.02em;
}
.top-bar-sub {
    font-size: 11px;
    color: #7D8590;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 1px;
}
.top-bar-badge {
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 500;
}
.badge-online  { background: #1B3A2A; color: #3FB950; border: 1px solid #238636; }
.badge-offline { background: #2D1B1B; color: #F85149; border: 1px solid #6E3130; }
.badge-idle    { background: #1C2230; color: #79C0FF; border: 1px solid #1F6FEB; }

/* ── KPI cards ── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.1rem; }
.kpi-card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 10px;
    padding: 0.85rem 1rem;
}
.kpi-label {
    font-size: 11px;
    color: #7D8590;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.kpi-sub {
    font-size: 11px;
    color: #7D8590;
    margin-top: 3px;
}
.kpi-green { color: #3FB950; }
.kpi-red   { color: #F85149; }
.kpi-blue  { color: #79C0FF; }
.kpi-amber { color: #D29922; }

/* ── Status alert boxes ── */
.status-clear {
    background: #1B3A2A;
    border: 1px solid #238636;
    color: #3FB950;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.status-alert {
    background: #2D1B1B;
    border: 1px solid #6E3130;
    color: #F85149;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(248,81,73,0.3); }
    70%  { box-shadow: 0 0 0 6px rgba(248,81,73,0); }
    100% { box-shadow: 0 0 0 0 rgba(248,81,73,0); }
}

/* ── Log panel ── */
.log-entry {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 3px 0;
    border-bottom: 1px solid #21262D;
    color: #7D8590;
}
.log-entry.corrosion { color: #F85149; }
.log-entry.clear     { color: #3FB950; }

/* ── Section headers ── */
.section-label {
    font-size: 11px;
    color: #7D8590;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    font-weight: 500;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0D1117;
    border-right: 1px solid #21262D;
}
[data-testid="stSidebar"] label { color: #C9D1D9 !important; font-size: 13px; }
[data-testid="stSidebar"] .stSlider label { color: #7D8590 !important; }

/* ── Altair chart container ── */
.vega-embed { border-radius: 8px; overflow: hidden; }

/* ── Fullscreen Image Modal ── */
.modal { display: none; position: fixed; z-index: 9999; padding-top: 40px; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.95); }
.modal-content { margin: auto; display: block; max-width: 90%; max-height: 85vh; border: 3px solid #3FB950; border-radius: 10px; box-shadow: 0 0 20px rgba(63, 185, 80, 0.4); }
#modalCaption { margin: auto; display: block; width: 80%; max-width: 700px; text-align: center; color: #E6EDF3; padding: 15px; height: auto; font-family: 'JetBrains Mono', monospace; font-size: 15px; background: #161B22; border-radius: 8px; margin-top: 15px; border: 1px solid #21262D; }
.close { position: absolute; top: 20px; right: 35px; color: #f1f1f1; font-size: 50px; font-weight: bold; transition: 0.3s; cursor: pointer; }
.close:hover, .close:focus { color: #F85149; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.gallery-item { position: relative; border-radius: 8px; overflow: hidden; border: 1px solid #21262D; cursor: pointer; transition: transform 0.2s; }
.gallery-item:hover { transform: scale(1.03); border-color: #79C0FF; }
.gallery-item img { width: 100%; height: 160px; object-fit: cover; display: block; }

/* ── Fullscreen Image Modal (Global) ── */
.modal { display: none; position: fixed; z-index: 99999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.95); overflow: auto; }
.modal-content { margin: 5% auto; display: block; max-width: 90%; max-height: 85vh; border: 3px solid #3FB950; border-radius: 10px; box-shadow: 0 0 40px rgba(63, 185, 80, 0.3); }
.modal-caption { margin: 15px auto; width: 90%; max-width: 600px; text-align: center; color: #E6EDF3; padding: 12px; font-family: 'JetBrains Mono', monospace; font-size: 14px; background: #161B22; border-radius: 8px; border: 1px solid #21262D; }
.modal-close { position: fixed; top: 20px; right: 35px; color: #f1f1f1; font-size: 50px; font-weight: bold; cursor: pointer; z-index: 100000; }
.modal-close:hover { color: #F85149; }
"""


def inject_css():
    """Call this once in main.py to apply all styles."""
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)