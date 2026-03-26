import streamlit as st
from auth import sign_up, sign_in

def show_login():
    # ── Back navigation ──
    st.markdown('<div class="lp-nav-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home"):
        st.session_state["page"] = "landing"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Header ──
    st.markdown("""
    <div style="text-align:center;padding:clamp(24px,5vw,56px) 20px 28px;">
        <p style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;color:#FFD700;
                  letter-spacing:3px;font-weight:700;margin:0 0 20px;">
            🏋️ IRONIQ
        </p>
        <h2 style="color:#e0e0e0;font-family:'Rajdhani',sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);
                   font-weight:700;margin:0 0 8px;letter-spacing:1px;">
            Welcome to IRONIQ
        </h2>
        <p style="color:#444;font-size:0.9rem;margin:0;">
            Sign in or create a free account to get started
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth form — centred ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            email    = st.text_input("Email address", key="login_email",       placeholder="you@example.com")
            password = st.text_input("Password",      key="login_password",    placeholder="••••••••", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login", use_container_width=True, key="login_btn"):
                if email and password:
                    res, err = sign_in(email, password)
                    if err:
                        st.error(f"Login failed: {err}")
                    else:
                        st.session_state["user"] = res.user
                        st.session_state["page"] = "app"
                        st.success("Welcome back! 💪")
                        st.rerun()
                else:
                    st.warning("Please enter email and password")

        with tab_signup:
            st.markdown("<br>", unsafe_allow_html=True)
            new_email        = st.text_input("Email address",         key="signup_email",    placeholder="you@example.com")
            new_password     = st.text_input("Password (min 6 chars)",key="signup_password", placeholder="••••••••", type="password")
            confirm_password = st.text_input("Confirm password",      key="confirm_password",placeholder="••••••••", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Free Account", use_container_width=True, key="signup_btn"):
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
                        st.success("✅ Account created! Please login now.")