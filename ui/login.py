import streamlit as st
from auth import sign_up, sign_in

def show_login():
    st.markdown("""
    <div class="hero-box">
        <h2>🏋️ FORGE YOUR STRENGTH</h2>
        <p>India's first AI powerlifting coach built for <strong style="color:#FFD700">Indian athletes</strong>.<br>
        Real food. Real programming. Real results.</p>
        <br>
        <div class="hero-stat"><div class="number">4</div><div class="label">Week Program</div></div>
        <div class="hero-stat"><div class="number">AI</div><div class="label">Personalized</div></div>
        <div class="hero-stat"><div class="number">🇮🇳</div><div class="label">Indian Diet</div></div>
        <div class="hero-stat"><div class="number">FREE</div><div class="label">Always</div></div>
    </div>
    """, unsafe_allow_html=True)



    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab_login:
            st.markdown("### Welcome back!")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", use_container_width=True):
                if email and password:
                    res, err = sign_in(email, password)
                    if err:
                        st.error(f"Login failed: {err}")
                    else:
                        st.session_state["user"] = res.user
                        st.success("Welcome back! 💪")
                        st.rerun()
                else:
                    st.warning("Please enter email and password")

        with tab_signup:
            st.markdown("### Create your account!")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            if st.button("Create Account", use_container_width=True):
                if not new_email or not new_password:
                    st.warning("Please fill all fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    res, err = sign_up(new_email, new_password)
                    if err:
                        st.error(f"Signup failed: {err}")
                    else:
                        st.success("✅ Account created! Please login.")