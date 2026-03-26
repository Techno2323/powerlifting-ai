import streamlit as st
from auth import sign_up, sign_in

def show_login():
    st.markdown("""
    <style>
    /* Login page — constrain form width on desktop, full width on mobile */
    .login-wrap {
        max-width: 480px;
        margin: 0 auto;
        width: 100%;
    }
    /* Back button — anchor link styled as outlined btn */
    .login-back-btn {
        display: inline-block;
        background: transparent;
        border: 1px solid #FFD70033;
        border-radius: 10px;
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.88rem; font-weight: 600;
        padding: 10px 20px; letter-spacing: 1px;
        text-decoration: none !important;
        transition: background 0.2s, border-color 0.2s;
        margin-bottom: 8px;
    }
    .login-back-btn:hover { background: #FFD70010 !important; border-color: #FFD70066 !important; }
    /* Login/Signup form buttons — full width */
    .login-wrap .stButton > button {
        width: 100% !important;
        min-height: 52px !important;
        font-size: 1rem !important;
    }
    @media (max-width: 640px) {
        .login-wrap { padding: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Back navigation ──
    st.markdown('<a href="?nav=landing" class="login-back-btn">← Back to Home</a>', unsafe_allow_html=True)

    # ── Header ──
    st.markdown("""
    <div style="text-align:center;padding:clamp(20px,5vw,48px) 0 24px;">
        <p style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;color:#FFD700;
                  letter-spacing:3px;font-weight:700;margin:0 0 16px;">
            🏋️ IRONIQ
        </p>
        <h2 style="color:#e0e0e0;font-family:'Rajdhani',sans-serif;font-size:clamp(1.5rem,4vw,2.2rem);
                   font-weight:700;margin:0 0 8px;letter-spacing:1px;">
            Welcome to IRONIQ
        </h2>
        <p style="color:#444;font-size:0.9rem;margin:0;">
            Sign in or create a free account to get started
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth form — centred via CSS, no columns ──
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        email    = st.text_input("Email address", key="login_email",    placeholder="you@example.com")
        password = st.text_input("Password",      key="login_password", placeholder="••••••••", type="password")
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
        new_email        = st.text_input("Email address",          key="signup_email",    placeholder="you@example.com")
        new_password     = st.text_input("Password (min 6 chars)", key="signup_password", placeholder="••••••••", type="password")
        confirm_password = st.text_input("Confirm password",       key="confirm_password",placeholder="••••••••", type="password")
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

    st.markdown('</div>', unsafe_allow_html=True)