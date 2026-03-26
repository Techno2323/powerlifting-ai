# app.py (updated)
import streamlit as st
import google.generativeai as genai
from auth import get_user
from ui.styles import load_css
from ui.landing import show_landing
from ui.login import show_login
from ui.dashboard import show_dashboard
from ui.generate import show_generate
from database import load_plan, load_logs

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(
    page_title="IRONIQ — Indian Powerlifting AI",
    page_icon="🏋️",
    layout="wide"
)

load_css()

# ── URL query param navigation (from HTML anchor links in landing page) ──
_nav = st.query_params.get("nav", "")
if _nav == "logout":
    st.query_params.clear()
    from auth import sign_out
    sign_out()
elif _nav in ("login", "landing", "app"):
    st.session_state["page"] = _nav
    st.query_params.clear()
    st.rerun()

# 🔑 Restore session from THIS browser's stored JWT
if "user" not in st.session_state and "_access_token" in st.session_state:
    try:
        user_data = get_user()
        if user_data:
            st.session_state["user"] = user_data.user
            st.session_state["page"] = "app"
        else:
            # Token expired/invalid
            st.session_state.pop("_access_token", None)
    except:
        st.session_state.pop("_access_token", None)

if "page" not in st.session_state:
    st.session_state["page"] = "landing"

user = st.session_state.get("user")

if user:
    # ── App header — pure HTML flex row, no columns ──
    st.markdown("""
    <style>
    .app-topbar {
        display: flex; align-items: center;
        justify-content: space-between;
        padding: 8px 0 16px;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 16px;
        gap: 10px;
    }
    .app-topbar-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(1.1rem, 3vw, 1.5rem);
        font-weight: 700; color: #FFD700;
        letter-spacing: 2px; margin: 0;
        white-space: nowrap; overflow: hidden;
        text-overflow: ellipsis;
    }
    .app-topbar-email {
        font-size: 0.72rem; color: #444;
        margin-top: 2px;
        white-space: nowrap; overflow: hidden;
        text-overflow: ellipsis; max-width: 200px;
    }
    .app-logout-btn { display: none !important; }
    .app-logout-html {
        background: transparent;
        border: 1px solid #ef444433;
        border-radius: 10px;
        color: #ef4444;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 8px 14px;
        cursor: pointer;
        white-space: nowrap;
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
        transition: background 0.2s, border-color 0.2s;
        flex-shrink: 0;
    }
    .app-logout-html:hover { background: #ef444412; border-color: #ef444466; }
    @media (max-width: 640px) {
        .app-topbar { padding: 6px 0 12px; }
        .app-topbar-email { max-width: 140px; }
    }
    </style>
    """, unsafe_allow_html=True)

    email_display = user.email if user.email else "User"
    st.markdown(f"""
    <div class="app-topbar">
        <div>
            <div class="app-topbar-title">🏋️ IRONIQ</div>
            <div class="app-topbar-email">{email_display}</div>
        </div>
        <a href="?nav=logout" class="app-logout-html">🚪 Logout</a>
    </div>
    """, unsafe_allow_html=True)

    plan_row = load_plan(user.id)
    log = load_logs(user.id)

    if plan_row is None:
        st.info("👋 No active plan found. Generate your first plan below!")
        show_generate(user.id)
    else:
        show_dashboard(user, plan_row, log)

elif st.session_state["page"] == "login":
    show_login()

else:
    show_landing()