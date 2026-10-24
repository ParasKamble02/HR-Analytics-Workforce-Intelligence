import streamlit as st


def load_styles():
    st.html("""
<style>
/* ---------- Layout ---------- */
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stMainBlockContainer"] { padding-top: 5rem !important; }
[data-testid="stMainBlockContainer"] h1 { padding-top: 0; margin-top: 0; }

/* ---------- Cards ---------- */
.insight-card { background: #151923; border: 1px solid #292f3d; border-radius: 16px; padding: 26px; min-height: 250px; box-sizing: border-box; }
.insight-title { color: #aab2c5; font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 25px; }
.insight-value { color: #ffffff; font-size: 22px; font-weight: 600; margin-bottom: 22px; }
.insight-text { color: #aab2c5; font-size: 14px; line-height: 1.6; }
.kpi-card { background: #151923; border: 1px solid #292f3d; border-radius: 16px; padding: 20px; }
.kpi-title { color: #aab2c5; font-size: 14px; }
.kpi-value { color: #ffffff; font-size: 28px; font-weight: 700; }
.kpi-subtitle { color: #8f98aa; font-size: 13px; }
.section-title { color: #ffffff; font-size: 24px; font-weight: 700; margin: 22px 0 12px 0; }
.section-title-tight { margin-top: 0; }

/* ---------- Inputs (main area) ---------- */
[data-testid="stMain"] [data-testid="stTextInput"] input { background: #151923; border: 1px solid #292f3d; border-radius: 12px; color: #ffffff; padding: 12px 14px; }
[data-testid="stMain"] [data-testid="stTextInput"] input:focus { border-color: #6366F1; box-shadow: 0 0 0 1px #6366F1; }
[data-testid="stMain"] [data-baseweb="select"] > div { background: #151923; border: 1px solid #292f3d; border-radius: 12px; }
[data-testid="stMain"] label p { color: #aab2c5; font-size: 13px; font-weight: 600; }

/* ---------- Table ---------- */
[data-testid="stDataFrame"] { border: 1px solid #292f3d; border-radius: 16px; overflow: hidden; }

/* ---------- Download button and records header row ---------- */
[data-testid="stDownloadButton"] { transform: translateY(16px); }
[data-testid="stDownloadButton"] button { background: linear-gradient(135deg, #3B82F6, #6366F1); color: #ffffff; border: none; border-radius: 12px; padding: 8px 18px; min-height: 44px; font-weight: 600; transition: all 0.2s ease; }
[data-testid="stDownloadButton"] button:hover { box-shadow: 0 4px 14px rgba(99, 102, 241, 0.45); transform: translateY(-1px); color: #ffffff; }
[data-testid="stDownloadButton"] button p { color: #ffffff; }
[data-testid="stHorizontalBlock"] .section-title { margin: 0; }
[data-testid="stHorizontalBlock"]:has([data-testid="stDownloadButton"]) { margin-top: 35px; margin-bottom: 6px; }

/* ---------- Insights page ---------- */
.finding-row { display: flex; align-items: center; gap: 16px; background: #151923; border: 1px solid #292f3d; border-radius: 14px; padding: 16px 20px; margin-bottom: 10px; }
.finding-num { min-width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; border-radius: 10px; font-size: 14px; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #3B82F6, #6366F1); }
.finding-text { color: #cbd1dc; font-size: 15px; line-height: 1.5; }
.reco-card { background: #151923; border: 1px solid #292f3d; border-left: 3px solid #6366F1; border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; min-height: 130px; box-sizing: border-box; }
.reco-card .insight-title { margin-bottom: 12px; }
.insight-note { text-align: center; color: #555d6e; font-size: 12px; margin-top: 30px; padding-top: 18px; border-top: 1px solid #20242e; }
.reco-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.reco-grid .reco-card { margin-bottom: 0; }
@media (max-width: 900px) { .reco-grid { grid-template-columns: 1fr; } }
            
/* ---------- Sidebar: container ---------- */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f121a 0%, #11141d 100%); border-right: 1px solid #20242e; }
[data-testid="stSidebar"][aria-expanded="true"] { width: 21rem !important; min-width: 21rem !important; max-width: 21rem !important; }
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child { width: 21rem !important; }
[data-testid="stSidebarResizeHandle"], [data-testid="stSidebar"] div[style*="col-resize"], [data-testid="stSidebar"] [class*="resize"] { display: none !important; pointer-events: none !important; }
[data-testid="stSidebarHeader"] { min-height: 0; height: 2.2rem; padding: 0.4rem 1rem 0 1rem; }
[data-testid="stSidebarUserContent"] { padding-top: 0 !important; padding-bottom: 0 !important; min-height: calc(100vh - 2.2rem); display: flex; flex-direction: column; }
[data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] { flex: 1; min-height: calc(100vh - 2.2rem); }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.4rem; }

/* ---------- Sidebar: brand card ---------- */
.sidebar-brand { display: flex; align-items: center; gap: 14px; padding: 14px 16px; margin: 8px 0 26px 0; background: #151923; border: 1px solid #292f3d; border-radius: 16px; }
.brand-icon { width: 40px; height: 40px; min-width: 40px; display: flex; align-items: center; justify-content: center; font-size: 19px; border-radius: 12px; background: linear-gradient(135deg, #3B82F6, #6366F1); box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35); }
.brand-title { color: #ffffff; font-size: 17px; font-weight: 700; line-height: 1.2; }
.brand-subtitle { color: #6b7385; font-size: 10px; letter-spacing: 1.6px; margin-top: 3px; }

/* ---------- Sidebar: labels and divider ---------- */
.sidebar-section-label { color: #7d8598; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 4px 0 10px 0; }
.sidebar-section-label::before { content: ""; display: inline-block; width: 3px; height: 12px; margin-right: 8px; vertical-align: -1px; border-radius: 2px; background: linear-gradient(180deg, #3B82F6, #6366F1); }
.sidebar-divider { height: 1px; margin: 22px 0; background: linear-gradient(90deg, transparent, #292f3d, transparent); }

/* ---------- Sidebar: navigation pills ---------- */
[data-testid="stSidebar"] div[role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] div[role="radiogroup"] > label { width: 100%; padding: 9px 14px; border-radius: 10px; border: 1px solid transparent; transition: all 0.2s ease; cursor: pointer; }
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: #151923; border-color: #292f3d; }
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(59, 130, 246, 0.18), rgba(99, 102, 241, 0.18)); border-color: #4f5bd5; }
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p { color: #ffffff; font-weight: 600; }

/* ---------- Sidebar: department filter ---------- */
[data-testid="stSidebar"] [data-baseweb="select"] > div { background: #151923; border: 1px solid #292f3d; border-radius: 12px; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background: linear-gradient(135deg, #3B82F6, #6366F1) !important; border-radius: 8px; font-size: 12px; height: 24px; margin: 2px; }

/* ---------- Sidebar: footer card ---------- */
[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sidebar-footer) { position: fixed; bottom: 40px; width: 16rem; max-width: calc(var(--sidebar-width, 21rem) - 3rem); margin: 0; }
.sidebar-footer { display: flex; align-items: center; gap: 10px; margin-top: 0; padding: 8px 12px; background: #151923; border: 1px solid #292f3d; border-radius: 12px; }
.footer-status { width: 8px; height: 8px; min-width: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.footer-title { color: #c8cdd8; font-size: 11px; font-weight: 600; }
.footer-text { color: #6b7385; font-size: 10px; margin-top: 1px; }
</style>
""")