import streamlit as st

def load_css():
    # ---- Inject viewport meta + floating background gym elements ----
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <div class="bg-gym-layer" aria-hidden="true">
        <span class="gym-float" style="left:5%;animation-delay:0s;animation-duration:20s;font-size:2.2rem">🏋️</span>
        <span class="gym-float" style="left:22%;animation-delay:-7s;animation-duration:25s;font-size:1.8rem">🏋️</span>
        <span class="gym-float" style="left:45%;animation-delay:-13s;animation-duration:18s;font-size:3rem">🏋️</span>
        <span class="gym-float" style="left:68%;animation-delay:-4s;animation-duration:22s;font-size:2rem">🏋️</span>
        <span class="gym-float" style="left:88%;animation-delay:-17s;animation-duration:28s;font-size:2.5rem">🏋️</span>
        <div class="gym-float plate" style="left:12%;animation-delay:-9s;animation-duration:30s;width:65px;height:65px"></div>
        <div class="gym-float plate" style="left:35%;animation-delay:-2s;animation-duration:38s;width:90px;height:90px"></div>
        <div class="gym-float plate" style="left:58%;animation-delay:-20s;animation-duration:26s;width:50px;height:50px"></div>
        <div class="gym-float plate" style="left:80%;animation-delay:-11s;animation-duration:32s;width:75px;height:75px"></div>
        <span class="gym-float" style="left:30%;animation-delay:-15s;animation-duration:17s;font-size:1.5rem;opacity:0.05">⚡</span>
        <span class="gym-float" style="left:72%;animation-delay:-6s;animation-duration:23s;font-size:1.8rem;opacity:0.05">⚡</span>
        <span class="gym-float" style="left:55%;animation-delay:-10s;animation-duration:19s;font-size:2rem;opacity:0.04">💪</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── RESET & BASE ── */
    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #080808;
        color: #d4d4d4;
        -webkit-font-smoothing: antialiased;
    }
    .stApp { background: #080808; min-height: 100vh; z-index: 1; position: relative; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── HIDDEN BUTTON SYSTEM ── */
    .st-hb { display: none !important; }
    div:has(.st-hb) + div {
        position: absolute !important;
        width: 1px !important; height: 1px !important;
        overflow: hidden !important; opacity: 0 !important;
        pointer-events: none !important; clip: rect(0,0,0,0) !important;
        margin: 0 !important; padding: 0 !important;
    }

    /* ── FIX: ONLY hide column resize bars, NOT inputs ── */
    [data-testid="stHorizontalBlock"] > .resize-handle,
    [data-testid="stHorizontalBlock"] [class*="resize"] {
        display: none !important;
    }

    /* Remove 300ms tap delay on all interactive elements */
    a, button, input, select, textarea,
    [role="button"], [tabindex] {
        touch-action: manipulation;
    }

    /* ── BLOCK CONTAINER ── */
    .block-container {
        max-width: 1100px !important;
        padding: 2rem 3rem !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
    }
    @media (max-width: 1200px) {
        .block-container { padding: 1.5rem 2rem !important; }
    }

    /* ── BACKGROUND GYM LAYER ── */
    .bg-gym-layer {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    .gym-float {
        position: absolute;
        bottom: -15%;
        opacity: 0;
        animation: gymFloat linear infinite;
        will-change: transform, opacity;
    }
    .plate {
        border-radius: 50%;
        border: 2px solid #FFD70018;
        box-shadow: inset 0 0 0 6px #080808,
                    inset 0 0 0 9px #FFD70010,
                    0 0 12px #FFD70008;
        background: transparent;
        font-size: 0;
    }
    @keyframes gymFloat {
        0%   { opacity: 0;    transform: translateY(0) rotate(0deg); }
        8%   { opacity: 0.07; }
        88%  { opacity: 0.05; }
        100% { opacity: 0;    transform: translateY(-115vh) rotate(25deg); }
    }

    /* ── ENSURE ALL INPUTS ARE VISIBLE ── */
    [data-testid="stNumberInput"],
    [data-testid="stSelectbox"],
    [data-testid="stTextInput"],
    [data-testid="stForm"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* ── TYPOGRAPHY ── */
    h1 {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: clamp(2rem, 6vw, 3.5rem) !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FFD700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 3s linear infinite;
        text-align: center;
        line-height: 1.1 !important;
    }
    @keyframes textShine { to { background-position: 200% center; } }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        font-size: clamp(1.1rem, 3.5vw, 1.8rem) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1.5px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        min-height: 48px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 4px 20px #FFD70033 !important;
        position: relative !important;
        overflow: hidden !important;
        touch-action: manipulation !important;
        -webkit-tap-highlight-color: transparent !important;
        z-index: 2;
    }
    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%; left: -75%;
        width: 50%; height: 200%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
        transform: skewX(-20deg);
        animation: shimmerBtn 3s infinite;
    }
    @keyframes shimmerBtn { 0% { left: -75%; } 100% { left: 150%; } }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 35px #FFD70055 !important;
    }
    .stButton > button:active {
        transform: translateY(0) scale(0.97) !important;
    }

    /* ── INPUTS ── */
    .stTextInput input {
        background: #111 !important;
        border: 1px solid #222 !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
        padding: 14px 16px !important;
        font-size: 16px !important;
        min-height: 48px !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
        touch-action: manipulation !important;
        z-index: 2;
    }
    .stTextInput input:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 3px #FFD70022 !important;
    }

    [data-testid="stNumberInput"] input {
        background: #0d0d0d !important;
        border: 1px solid #FFD70030 !important;
        border-radius: 10px !important;
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        min-height: 52px !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
        touch-action: manipulation !important;
        z-index: 2;
    }
    [data-testid="stNumberInput"] input:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 3px #FFD70022 !important;
    }

    [data-testid="stNumberInput"] button {
        min-width: 44px !important;
        min-height: 44px !important;
        touch-action: manipulation !important;
        z-index: 2;
    }

    [data-testid="stSelectbox"] > div > div {
        background: #111 !important;
        border: 1px solid #222 !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
        min-height: 48px !important;
        font-size: 16px !important;
        z-index: 2;
    }
    [data-testid="stSelectbox"] > div > div:hover { border-color: #FFD70044 !important; }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #0f0f0f !important;
        border-radius: 14px !important;
        padding: 5px !important;
        border: 1px solid #1a1a1a !important;
        gap: 4px !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
        -webkit-overflow-scrolling: touch !important;
        z-index: 2;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
    .stTabs [data-baseweb="tab"] {
        color: #444 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        white-space: nowrap !important;
        min-height: 44px !important;
        transition: color 0.2s !important;
        touch-action: manipulation !important;
        -webkit-tap-highlight-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        box-shadow: 0 2px 12px #FFD70044 !important;
    }

    /* ── METRICS ── */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #141414, #101010) !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 16px !important;
        padding: 20px 16px !important;
        text-align: center !important;
        transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s !important;
        box-shadow: 0 4px 20px #00000055 !important;
        animation: cardIn 0.5s ease both;
        z-index: 2;
    }
    @keyframes cardIn {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    [data-testid="metric-container"]:hover {
        border-color: #FFD70044 !important;
        box-shadow: 0 8px 32px #FFD70022 !important;
        transform: translateY(-4px) !important;
    }
    [data-testid="metric-container"] label {
        color: #555 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-weight: 500 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: clamp(1.5rem, 4vw, 2.2rem) !important;
        font-weight: 700 !important;
    }

    /* ── PROGRESS BARS ── */
    [role="progressbar"] {
        background: #1a1a1a !important;
        border-radius: 20px !important;
        height: 8px !important;
        overflow: hidden !important;
        border: none !important;
        z-index: 2;
    }
    [role="progressbar"] > div {
        background: linear-gradient(90deg, #B8860B, #FFD700, #FFA500, #FFD700) !important;
        background-size: 300% 100% !important;
        border-radius: 20px !important;
        height: 8px !important;
        animation: barShimmer 2.5s linear infinite, barGlow 2s ease-in-out infinite !important;
        box-shadow: 0 0 10px #FFD70055 !important;
        border: none !important;
    }
    .stProgress p,
    .stProgress > div > p,
    .stProgress small {
        color: #555 !important;
        font-size: 0.78rem !important;
        margin-top: 6px !important;
        margin-bottom: 0 !important;
        display: block !important;
    }
    @keyframes barShimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }
    @keyframes barGlow { 0%,100% { box-shadow: 0 0 8px #FFD70055; } 50% { box-shadow: 0 0 18px #FFD700aa; } }

    /* ── EXERCISE CARDS ── */
    .ex-card {
        background: linear-gradient(145deg, #131313, #0e0e0e);
        border: 1px solid #1c1c1c;
        border-left: 3px solid #FFD700;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        animation: cardIn 0.4s ease both;
        z-index: 2;
    }
    .ex-card:hover {
        transform: translateX(5px);
        border-color: #FFD70055;
        box-shadow: 0 4px 20px #FFD70015;
    }
    .ex-name {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #e8e8e8;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 6px;
    }
    .ex-weight-tag {
        background: #FFD70015;
        border: 1px solid #FFD70030;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.8rem;
        color: #FFD700;
        font-weight: 600;
        white-space: nowrap;
    }
    .ex-meta { color: #555; font-size: 0.8rem; margin-top: 5px; letter-spacing: 0.3px; }
    .ex-note { color: #777; font-size: 0.8rem; font-style: italic; margin-top: 5px; line-height: 1.5; }

    /* ── SCHEDULE ITEMS ── */
    .schedule-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 6px;
        background: #0e0e0e;
        border: 1px solid #181818;
        transition: background 0.2s, border-color 0.2s;
        -webkit-tap-highlight-color: transparent;
        z-index: 2;
    }
    .schedule-item:hover { background: #121212; border-color: #222; }
    .schedule-item.today {
        border-color: #FFD70044 !important;
        background: #FFD70008 !important;
        box-shadow: 0 0 0 1px #FFD70022;
    }
    .schedule-item.completed {
        border-color: #22c55e22 !important;
        background: #09120900 !important;
        opacity: 0.85;
    }
    .schedule-item.missed {
        border-color: #ef444422 !important;
        opacity: 0.6;
    }

    /* ── BLOCKQUOTE FALLBACK ── */
    blockquote {
        background: #111 !important;
        border-left: 3px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin: 8px 0 !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        z-index: 2;
    }
    blockquote:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 4px 20px #FFD70015 !important;
    }

    /* ── FORMS ── */
    [data-testid="stForm"] {
        background: #0d0d0d !important;
        border: 1px solid #1e1e1e !important;
        border-radius: 16px !important;
        padding: 22px !important;
        z-index: 2;
        position: relative;
    }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] {
        background: #0f0f0f !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] button {
        color: #999 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: color 0.2s !important;
    }
    [data-testid="stExpander"] button:hover { color: #FFD700 !important; }

    /* ── ERRORS / ALERTS ── */
    .stError, [data-testid="stAlert"] {
        background: #2a1a1a !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        color: #ff9999 !important;
        font-size: 0.9rem !important;
    }

    .stSuccess {
        background: #1a2a1a !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        color: #99ff99 !important;
        font-size: 0.9rem !important;
    }

    .stWarning {
        background: #2a2a1a !important;
        border-left: 4px solid #eab308 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        color: #ffff99 !important;
        font-size: 0.9rem !important;
    }

    .stInfo {
        background: #1a2a2a !important;
        border-left: 4px solid #06b6d4 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        color: #99ffff !important;
        font-size: 0.9rem !important;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .block-container { padding: 1rem 1.5rem !important; }
        h1 { font-size: clamp(1.5rem, 5vw, 2.5rem) !important; }
        .stButton > button { min-height: 44px; font-size: 0.9rem; }
        [data-testid="stNumberInput"] input { font-size: 1.2rem; }
    }

    /* ── GEN PAGE SPECIFIC ── */
    .gen-header { text-align: center; padding: 20px 0; z-index: 2; position: relative; }
    .gen-title { font-family: 'Rajdhani', sans-serif; font-size: clamp(1.8rem, 5vw, 2.5rem); font-weight: 700; color: #FFD700; margin-bottom: 8px; }
    .gen-subtitle { color: #666; font-size: 1rem; margin-bottom: 24px; }
    .gen-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-top: 24px; z-index: 2; position: relative; }
    .gen-card { background: #111; border: 1px solid #FFD70030; border-radius: 12px; padding: 20px; text-align: center; transition: all 0.2s; }
    .gen-card:hover { border-color: #FFD700; transform: translateY(-4px); box-shadow: 0 8px 24px #FFD70015; }
    .gen-card-icon { font-size: 2.5rem; display: block; margin-bottom: 8px; }
    .gen-card-name { font-family: 'Rajdhani', sans-serif; font-weight: 700; color: #FFD700; font-size: 0.9rem; letter-spacing: 1px; margin-bottom: 4px; }
    .gen-card-sub { color: #555; font-size: 0.75rem; }
    </style>
    """, unsafe_allow_html=True)