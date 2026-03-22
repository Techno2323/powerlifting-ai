import streamlit as st
import google.generativeai as genai
from auth import get_user
from ui.styles import load_css
from ui.login import show_login
from ui.dashboard import show_dashboard
from ui.generate import show_generate
from database import load_plan, load_logs

# ---- Init ----
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(
    page_title="Indian Powerlifting AI Coach",
    page_icon="🏋️",
    layout="wide"
)

# ---- Load CSS globally ----
load_css()

# ---- Session Check ----
if "user" not in st.session_state:
    try:
        user_data = get_user()
        if user_data:
            st.session_state["user"] = user_data.user
    except:
        pass

# ---- Router ----
if "user" in st.session_state and st.session_state["user"]:
    user = st.session_state["user"]

    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🏋️ Indian Powerlifting AI Coach")
        st.caption(f"Welcome, {user.email} 👋")
    with col2:
        if st.button("🚪 Logout"):
            from auth import sign_out
            sign_out()

    plan_row = load_plan(user.id)
    log = load_logs(user.id)

    if plan_row is None:
        st.info("👋 No active plan found. Generate your first plan below!")
        show_generate(user.id)
    else:
        show_dashboard(user, plan_row, log)

elif st.session_state.get("page") == "login":
    show_login()

else:
    from ui.landing import show_landing
    show_landing()