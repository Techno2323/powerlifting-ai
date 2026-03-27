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

    /* ── COLUMN RESIZE HANDLES — removed aggressive hide rule that broke form inputs ── */
    /* Streamlit's internal resize handle is 8px wide and purely cosmetic; no override needed */

    /* Remove 300ms tap delay on all interactive elements */
    a, button, input, select, textarea,
    [role="button"], [tabindex] {
        touch-action: manipulation;
    }

    /* ── BLOCK CONTAINER — cap width, reduce Streamlit's excess padding ── */
    .block-container {
        max-width: 1100px !important;
        padding: 2rem 3rem !important;
        margin: 0 auto !important;
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

    /* ── GENERATE PAGE HEADER ── */
    .gen-header {
        background: linear-gradient(135deg, #111, #0d0d0d);
        border: 1px solid #FFD70020;
        border-radius: 20px;
        padding: clamp(20px, 5vw, 40px);
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 0 40px #FFD70008;
        animation: heroIn 0.6s ease both;
    }
    .gen-title {
        color: #FFD700;
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(1.2rem, 4vw, 2rem);
        font-weight: 700;
        letter-spacing: 3px;
        margin: 0;
    }
    .gen-subtitle {
        color: #444;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
    }
    .gen-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 24px;
    }
    .gen-card {
        background: #0a0a0a;
        border: 1px solid #FFD70020;
        border-radius: 14px;
        padding: 20px 14px;
        text-align: center;
        transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
    }
    .gen-card:hover { transform: translateY(-5px); border-color: #FFD70055; box-shadow: 0 8px 30px #FFD70015; }
    .gen-card-icon {
        font-size: 2.2rem;
        display: block;
        margin-bottom: 8px;
        animation: iconBounce 2.5s ease-in-out infinite;
    }
    .gen-card:nth-child(2) .gen-card-icon { animation-delay: 0.35s; }
    .gen-card:nth-child(3) .gen-card-icon { animation-delay: 0.7s; }
    @keyframes iconBounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
    .gen-card-name { color: #FFD700; font-weight: 700; letter-spacing: 2px; font-family: 'Rajdhani', sans-serif; font-size: 1rem; }
    .gen-card-sub  { color: #444; font-size: 0.72rem; margin-top: 4px; }

    /* ── PROGRESS DASHBOARD ── */
    .progress-header {
        text-align: center;
        padding: 20px 0 28px;
        animation: heroIn 0.6s ease both;
    }
    .progress-title {
        font-family: 'Rajdhani', sans-serif;
        color: #FFD700;
        font-size: clamp(1.2rem, 4vw, 2rem);
        font-weight: 700;
        letter-spacing: 3px;
        margin: 0;
    }
    .progress-sub {
        color: #444;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
    }
    .lift-pr-card {
        background: linear-gradient(145deg, #141414, #101010);
        border: 1px solid #FFD70022;
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        animation: cardIn 0.5s ease both;
        position: relative;
        overflow: hidden;
    }
    .lift-pr-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at top, #FFD70008 0%, transparent 70%);
        pointer-events: none;
    }
    .lift-pr-card:hover {
        transform: translateY(-5px);
        border-color: #FFD70055;
        box-shadow: 0 10px 40px #FFD70020;
    }
    .lift-pr-icon {
        font-size: 1.6rem;
        display: block;
        margin-bottom: 10px;
        animation: iconBounce 3s ease-in-out infinite;
    }
    .lift-pr-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.7rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    .lift-pr-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        color: #FFD700;
        font-weight: 700;
        line-height: 1;
    }
    .lift-pr-delta {
        font-size: 0.78rem;
        margin-top: 6px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }
    .lift-pr-delta.positive { color: #22c55e; }
    .lift-pr-delta.negative { color: #ef4444; }
    .lift-pr-delta.neutral  { color: #555; }
    .chart-section {
        background: linear-gradient(145deg, #0d0d0d, #0a0a0a);
        border: 1px solid #1a1a1a;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        animation: cardIn 0.5s ease both;
    }
    .chart-title {
        font-family: 'Rajdhani', sans-serif;
        color: #FFD700;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .empty-progress {
        text-align: center;
        padding: 60px 20px;
        animation: heroIn 0.6s ease both;
    }
    .empty-progress .empty-icon { font-size: 3.5rem; margin-bottom: 16px; display: block; }
    .empty-progress h3 {
        color: #888;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .empty-progress p { color: #444; font-size: 0.88rem; line-height: 1.6; }
    .session-table-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 60px 70px;
        gap: 8px;
        padding: 10px 14px;
        border-radius: 10px;
        border: 1px solid #181818;
        background: #0e0e0e;
        margin-bottom: 6px;
        font-size: 0.82rem;
        transition: background 0.2s;
    }
    .session-table-row:hover { background: #121212; }
    .session-table-head {
        color: #555;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #080808; }
    ::-webkit-scrollbar-thumb { background: #FFD70044; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #FFD70099; }

    /* ══════════════════════════
       MOBILE — max 640px
    ══════════════════════════ */
    @media (max-width: 640px) {
        /* Safe area insets for notched phones */
        .block-container {
            padding: 1rem 1rem 2rem !important;
            padding-left: max(1rem, env(safe-area-inset-left)) !important;
            padding-right: max(1rem, env(safe-area-inset-right)) !important;
            padding-bottom: max(2rem, env(safe-area-inset-bottom)) !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }

        /* Hide Streamlit column resize handles */
        [data-testid="column"] > div:first-child::after { display: none !important; }

        /* Stack Streamlit columns — ONLY for multi-column rows in forms/dashboards.
           NOT applied globally so it doesn't break single-col layouts */
        [data-testid="stForm"] [data-testid="stHorizontalBlock"],
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 6px !important;
        }
        [data-testid="stForm"] [data-testid="column"],
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        /* Tabs scroll */
        .stTabs [data-baseweb="tab-list"] { justify-content: flex-start !important; }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.78rem !important;
            padding: 10px 12px !important;
            min-height: 44px !important;
        }

        /* Buttons — full width ONLY inside forms and tab panels, NOT globally */
        [data-testid="stForm"] .stButton > button,
        [data-testid="stFormSubmitButton"] button,
        [data-baseweb="tab-panel"] .stButton > button {
            width: 100% !important;
            padding: 16px !important;
            font-size: 1rem !important;
            min-height: 52px !important;
        }

        /* Number inputs */
        [data-testid="stNumberInput"] input {
            font-size: 1.3rem !important;
            min-height: 56px !important;
        }

        /* Title */
        h1 { font-size: 1.8rem !important; }

        /* Generate cards: 1 column on mobile */
        .gen-cards { grid-template-columns: 1fr !important; gap: 10px !important; }
        .gen-card { padding: 14px !important; }
        .gen-card-icon { font-size: 1.8rem !important; }

        /* Hero stat row */
        .hero-stats-row { gap: 8px !important; }
        .hero-stat { padding: 10px 12px !important; min-width: 64px !important; }
        .hero-stat .number { font-size: 1.3rem !important; }

        /* Reduce floating elements on mobile (performance) */
        .gym-float { will-change: auto !important; animation: none !important; opacity: 0 !important; }

        /* Exercise cards */
        .ex-name { font-size: 0.95rem !important; }
        .ex-card { padding: 12px 14px !important; margin-bottom: 8px !important; }
        .ex-card:hover { transform: none !important; }

        /* Schedule items */
        .schedule-item { padding: 10px 12px !important; gap: 8px !important; }

        /* Metrics */
        [data-testid="metric-container"] { padding: 14px 10px !important; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1.4rem !important; }

        /* Form inner padding */
        [data-testid="stForm"] { padding: 14px !important; border-radius: 14px !important; }

        /* Expander */
        [data-testid="stExpander"] summary { min-height: 56px !important; padding: 0 14px !important; }

        /* Slider thumb */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            width: 32px !important;
            height: 32px !important;
        }

        /* Gen header */
        .gen-header { padding: 16px !important; }
        .gen-title { letter-spacing: 1.5px !important; }
    }

    /* ══════════════════════════
       ULTRA-SMALL — max 390px
    ══════════════════════════ */
    @media (max-width: 390px) {
        .block-container { padding: 0.75rem !important; }
        h1 { font-size: 1.5rem !important; }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.72rem !important;
            padding: 8px 10px !important;
        }
        .ex-card { padding: 10px 12px !important; }
        [data-testid="metric-container"] { padding: 12px 8px !important; }
        [data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
    }

    /* ══════════════════════════
       TABLET — 641-1024px
    ══════════════════════════ */
    @media (min-width: 641px) and (max-width: 1024px) {
        .block-container { padding: 1.5rem !important; }
        .gen-cards { grid-template-columns: repeat(3, 1fr) !important; }
    }
    </style>
    """, unsafe_allow_html=True)