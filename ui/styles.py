import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0a0a0a;
        color: #e0e0e0;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #111111 50%, #0d0d0d 100%);
    }

    #MainMenu, footer, header {visibility: hidden;}

    h1 {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: center;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }

    .hero-box {
        background: linear-gradient(135deg, #1a1a1a, #111);
        border: 1px solid #FFD70033;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 40px #FFD70011;
        animation: fadeInUp 0.8s ease;
    }

    .hero-stat {
        display: inline-block;
        background: #FFD70011;
        border: 1px solid #FFD70033;
        border-radius: 12px;
        padding: 15px 25px;
        margin: 8px;
        text-align: center;
    }

    .hero-stat .number {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2rem;
        color: #FFD700;
        font-weight: 700;
    }

    .hero-stat .label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px #FFD70033 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px #FFD70055 !important;
    }

    .stTextInput input {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #fff !important;
        padding: 12px !important;
        transition: border 0.3s ease;
    }

    .stTextInput input:focus {
        border: 1px solid #FFD700 !important;
        box-shadow: 0 0 10px #FFD70033 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #111;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #222;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
    }

    [data-testid="metric-container"] {
        background: #1a1a1a;
        border: 1px solid #FFD70022;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px #00000055;
    }

    [data-testid="metric-container"]:hover {
        border-color: #FFD700;
        box-shadow: 0 0 20px #FFD70033;
        transform: translateY(-3px);
    }

    [data-testid="metric-container"] label {
        color: #888 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 10px #FFD70066 !important;
        animation: glowPulse 2s infinite;
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 10px #FFD70066; }
        50% { box-shadow: 0 0 20px #FFD700aa; }
    }

    blockquote {
        background: #1a1a1a !important;
        border-left: 3px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
    }

    blockquote:hover {
        background: #222 !important;
        box-shadow: 0 4px 20px #FFD70022 !important;
        transform: translateX(5px) !important;
    }

    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        color: #FFD700 !important;
        font-weight: 600 !important;
    }

    .stSuccess {
        background: #0a1f0a !important;
        border: 1px solid #00ff0033 !important;
        border-radius: 12px !important;
    }

    .stInfo {
        background: #1a1500 !important;
        border: 1px solid #FFD70033 !important;
        border-radius: 12px !important;
    }

    hr {
        border-color: #FFD70022 !important;
        margin: 20px 0 !important;
    }

    [data-testid="stForm"] {
        background: #111 !important;
        border: 1px solid #FFD70022 !important;
        border-radius: 0 0 20px 20px !important;
        padding: 20px 30px !important;
    }

    [data-testid="stNumberInput"] input {
        background: #0d0d0d !important;
        border: 1px solid #FFD70033 !important;
        border-radius: 10px !important;
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }

    [data-testid="stSelectbox"] > div > div {
        background: #0d0d0d !important;
        border: 1px solid #FFD70033 !important;
        border-radius: 10px !important;
        color: #fff !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #111; }
    ::-webkit-scrollbar-thumb { background: #FFD70066; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #FFD700; }
    </style>
    """, unsafe_allow_html=True)