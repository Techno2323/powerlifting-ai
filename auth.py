# auth.py
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
        # 🔑 CRITICAL: Store JWT in session_state, not in the shared client
        if res and res.session:
            st.session_state["_access_token"] = res.session.access_token
            st.session_state["_refresh_token"] = res.session.refresh_token
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
    try:
        return supabase.auth.get_user()
    except:
        return None