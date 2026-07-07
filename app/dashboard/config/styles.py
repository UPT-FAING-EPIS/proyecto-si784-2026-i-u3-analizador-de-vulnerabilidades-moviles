"""
AnzenCore – CSS styles injected into Streamlit via st.markdown.
"""

GLOBAL_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root palette ── */
:root {
    --cyan:    #00d4ff;
    --cyan-dim:#0096b4;
    --green:   #00ff88;
    --red:     #ff4757;
    --orange:  #ffa502;
    --yellow:  #ffdd59;
    --bg:      #0a0e1a;
    --bg2:     #111827;
    --bg3:     #1a2235;
    --border:  rgba(0,212,255,.18);
    --text:    #e2e8f0;
    --muted:   #64748b;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--cyan-dim); border-radius: 3px; }

/* ── Animaciones Base ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(0, 212, 255, 0.2); }
    50% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }
    100% { box-shadow: 0 0 10px rgba(0, 212, 255, 0.2); }
}

/* ── Cards / glass panels ── */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stForm"] {
    background: linear-gradient(135deg, rgba(17,24,39,.9) 0%, rgba(26,34,53,.9) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(12px);
    animation: fadeInUp 0.6s ease-out forwards;
}

/* ── Metrics ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #111827 0%, #1a2235 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    transition: transform .2s, border-color .2s;
    animation: fadeInUp 0.5s ease-out forwards;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: var(--cyan) !important;
    animation: pulseGlow 1.5s infinite;
}
div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stMetricLabel"] {
    font-size: .75rem !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
    color: var(--muted) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #00d4ff11) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--cyan) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: .85rem !important;
    letter-spacing: .04em !important;
    padding: .55rem 1.25rem !important;
    transition: all .2s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff44, #00d4ff22) !important;
    box-shadow: 0 0 20px rgba(0,212,255,.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00ff8822, #00ff8811) !important;
    color: var(--green) !important;
    border: 1px solid var(--green) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 20px rgba(0,255,136,.25) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stFileUploader > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
    font-size: .85rem !important;
    padding: .4rem 1rem !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00d4ff22, #00d4ff11) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--cyan) !important;
}

/* ── Dataframe / table ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
.stDataFrame table { font-family: 'JetBrains Mono', monospace !important; font-size: .8rem !important; }
.stDataFrame thead th {
    background: var(--bg3) !important;
    color: var(--cyan) !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    font-size: .7rem !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: border-color .2s !important;
}
.streamlit-expanderHeader:hover { border-color: var(--cyan) !important; }
.streamlit-expanderContent {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stButton > button {
    color: var(--cyan) !important;
    border-color: var(--cyan) !important;
    background: rgba(0,212,255,.08) !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 0 20px rgba(0,212,255,.25) !important;
}

/* ── Sidebar nav items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: .65rem;
    padding: .6rem .9rem;
    margin: .2rem 0;
    border-radius: 9px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all .18s ease;
    font-size: .88rem;
    font-weight: 500;
    color: var(--muted);
    background: transparent;
    text-decoration: none;
    user-select: none;
}
.nav-item:hover {
    background: rgba(0,212,255,.07);
    border-color: rgba(0,212,255,.2);
    color: var(--text);
}
.nav-item.active {
    background: linear-gradient(90deg, rgba(0,212,255,.15), rgba(0,212,255,.05));
    border-color: rgba(0,212,255,.4);
    color: var(--cyan);
    font-weight: 600;
}
.nav-item .nav-icon {
    font-size: 1.05rem;
    width: 1.4rem;
    text-align: center;
    flex-shrink: 0;
}
.nav-section-label {
    font-size: .65rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: var(--muted);
    padding: .8rem .9rem .3rem;
    opacity: .7;
}
/* Override Streamlit button inside nav to look like nav items */
section[data-testid="stSidebar"] .nav-btn > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--muted) !important;
    border-radius: 9px !important;
    font-size: .88rem !important;
    font-weight: 500 !important;
    padding: .6rem .9rem !important;
    text-align: left !important;
    width: 100% !important;
    transition: all .18s ease !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .nav-btn > button:hover {
    background: rgba(0,212,255,.07) !important;
    border-color: rgba(0,212,255,.2) !important;
    color: var(--text) !important;
    transform: none !important;
}
section[data-testid="stSidebar"] .nav-btn-active > button {
    background: linear-gradient(90deg, rgba(0,212,255,.15), rgba(0,212,255,.05)) !important;
    border-color: rgba(0,212,255,.4) !important;
    color: var(--cyan) !important;
    font-weight: 600 !important;
}
/* Page breadcrumb */
.page-header {
    display: flex;
    align-items: center;
    gap: .65rem;
    padding: .6rem 1rem;
    background: rgba(0,212,255,.05);
    border: 1px solid rgba(0,212,255,.15);
    border-radius: 10px;
    margin-bottom: 1.25rem;
    font-size: .85rem;
    color: var(--muted);
}
.page-header span { color: var(--cyan); font-weight: 600; }

/* ── Info / Success / Error / Warning banners ── */
.stAlert { border-radius: 10px !important; border-left-width: 4px !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--cyan) !important; }

/* ── Headings ── */
h1 { 
    font-size: 1.9rem !important; 
    font-weight: 800 !important;
    background: linear-gradient(90deg, var(--cyan), var(--green));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -.02em !important;
    margin-bottom: .5rem !important;
}
h2, h3 {
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -.01em !important;
}
h2::before { content: '// '; color: var(--cyan); font-size: .9em; }

/* ── Ocultar hipervínculos de ancla en títulos ── */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
h1 a:hover, h2 a:hover, h3 a:hover {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
[data-testid="stHeadingWithActionElements"] a,
[data-testid="stHeadingWithActionElements"] svg {
    display: none !important;
    visibility: hidden !important;
}

/* ── Code blocks ── */
code, pre {
    background: #0d1321 !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--green) !important;
    font-size: .8rem !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    border: 2px dashed var(--border) !important;
    border-radius: 10px !important;
    transition: border-color .2s !important;
}
.stFileUploader > div:hover { border-color: var(--cyan) !important; }

/* ── Badge-style severity pills ── */
.badge-critico  { color: #ff4757; font-weight: 700; }
.badge-alto     { color: #ffa502; font-weight: 700; }
.badge-medio    { color: #ffdd59; font-weight: 700; }
.badge-bajo     { color: #00ff88; font-weight: 700; }
.badge-info     { color: #00d4ff; font-weight: 700; }

/* ── Pulse animation for online dot ── */
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(0,255,136,.5); }
    70%  { box-shadow: 0 0 0 8px rgba(0,255,136,0); }
    100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
}
.online-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--green);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
    margin-right: 6px;
    vertical-align: middle;
}

/* ── Login card ── */
.login-card {
    max-width: 440px;
    margin: 3rem auto;
    background: linear-gradient(135deg, rgba(17,24,39,.95) 0%, rgba(26,34,53,.95) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 60px rgba(0,0,0,.5), 0 0 0 1px rgba(0,212,255,.05);
}
.login-logo {
    text-align: center;
    font-size: 3rem;
    margin-bottom: .5rem;
}
.login-title {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--cyan), var(--green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: .25rem;
}
.login-subtitle {
    text-align: center;
    color: var(--muted);
    font-size: .85rem;
    margin-bottom: 1.5rem;
}

/* ════════════════════════════════════════════════════════
   RESPONSIVE – Breakpoints
   ≥ 1280px  → Desktop full (default above)
     768-1279px → Laptop / Tablet landscape
   < 768px   → Tablet portrait / Mobile
   < 480px   → Mobile small
   ════════════════════════════════════════════════════════ */

/* ── Laptop / Tablet landscape (768 – 1279px) ─────────── */
@media (max-width: 1279px) {
    .block-container {
        padding: 1.25rem 1.25rem 2.5rem !important;
        max-width: 100% !important;
    }
    h1 { font-size: 1.55rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
}

/* ── Tablet portrait / Mobile (< 768px) ───────────────── */
@media (max-width: 767px) {
    /* Contenedor principal más compacto */
    .block-container {
        padding: 1rem .75rem 2rem !important;
    }

    /* Ocultar sidebar collapse button text */
    section[data-testid="stSidebar"] { min-width: 0 !important; }

    /* Columnas de Streamlit → pasan a ser filas */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: .6rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: calc(50% - .6rem) !important;
        flex: 1 1 calc(50% - .6rem) !important;
    }

    /* En el login, forzar a que las columnas se apilen al 100% y se centren con un ancho máximo de 440px */
    div:has(.login-card) [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    div:has(> .login-card) ~ [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
        max-width: 440px !important;
        margin: 0 auto !important;
    }

    /* Métricas en 2 columnas */
    div[data-testid="stMetric"] {
        padding: .75rem 1rem !important;
    }
    div[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    div[data-testid="stMetricLabel"] { font-size: .7rem !important; }

    /* Headings más pequeños */
    h1 { font-size: 1.35rem !important; }
    h2 { font-size: 1.1rem !important; }

    /* Login card ocupa todo el ancho */
    .login-card {
        max-width: 100% !important;
        margin: 1rem .5rem !important;
        padding: 1.5rem !important;
        border-radius: 14px !important;
    }
    .login-logo { font-size: 2.2rem !important; }
    .login-title { font-size: 1.25rem !important; }

    /* Botones: altura mínima para touch */
    .stButton > button,
    .stDownloadButton > button {
        min-height: 2.6rem !important;
        font-size: .9rem !important;
        padding: .6rem 1rem !important;
    }

    /* Tabs: texto más compacto */
    .stTabs [data-baseweb="tab"] {
        font-size: .78rem !important;
        padding: .35rem .65rem !important;
    }

    /* Dataframe: scroll horizontal */
    .stDataFrame {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    .stDataFrame table { font-size: .72rem !important; }

    /* Alertas */
    .stAlert { font-size: .85rem !important; }

    /* Expanders */
    .streamlit-expanderHeader { font-size: .85rem !important; }

    /* Online users: 2 por fila */
    [data-testid="stHorizontalBlock"] .online-card {
        min-width: calc(50% - .5rem) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding: .75rem !important;
    }
}

/* ── Mobile pequeño (< 480px) ─────────────────────────── */
@media (max-width: 479px) {
    .block-container { padding: .75rem .5rem 2rem !important; }

    /* Columnas → 100% ancho (una por fila) */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Métricas 1 por fila */
    div[data-testid="stMetric"] { padding: .6rem .75rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1.25rem !important; }

    h1 { font-size: 1.2rem !important; }
    h2 { font-size: 1rem !important; }

    /* Login card sin margen lateral */
    .login-card {
        margin: .5rem 0 !important;
        border-radius: 10px !important;
        padding: 1.25rem !important;
    }

    /* Tabs: wrap si no caben */
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: wrap !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: .75rem !important;
        padding: .3rem .5rem !important;
    }

    /* Botones touch-friendly */
    .stButton > button,
    .stDownloadButton > button {
        min-height: 3rem !important;
        font-size: .85rem !important;
        width: 100% !important;
    }

    /* Inputs más grandes */
    .stTextInput > div > div > input {
        font-size: 1rem !important;
        padding: .65rem .9rem !important;
    }

    /* Código más pequeño */
    code, pre { font-size: .72rem !important; }
}

/* ── Viewport meta fallback (inyectado vía JS) ────────── */
/* Asegura que el viewport esté configurado correctamente en móviles */
</style>
"""


VIEWPORT_META = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
"""


def inject_css() -> None:
    """Call once at app startup to inject all custom styles."""
    import streamlit as st
    st.markdown(VIEWPORT_META, unsafe_allow_html=True)
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ── Helper: severity color tag ──────────────────────────────────────────────
SEVERITY_ICON = {
    "Critico": "🔴",
    "Alto":    "🟠",
    "Medio":   "🟡",
    "Bajo":    "🟢",
    "Info":    "🔵",
}


def severity_icon(level: str) -> str:
    return SEVERITY_ICON.get(level, "⚪")
