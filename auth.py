import streamlit as st
from database import supabase

def sign_up(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        # Store the access token in session_state so each browser session
        # validates independently — avoids module-level singleton bleed
        if res and res.session:
            st.session_state["_access_token"] = res.session.access_token
        return res, None
    except Exception as e:
        return None, str(e)

def sign_out():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.clear()
    st.rerun()

def get_user():
    """
    Validate the user using the JWT stored in THIS browser's session_state.
    Never reads from the shared Supabase client's internal session —
    that would bleed across concurrent users.
    """
    token = st.session_state.get("_access_token")
    if not token:
        return None
    try:
        return supabase.auth.get_user(token)
    except:
        # Token expired or invalid — clear it
        st.session_state.pop("_access_token", None)
        return None