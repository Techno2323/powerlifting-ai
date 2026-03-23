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
        return res, None
    except Exception as e:
        return None, str(e)

def sign_out():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()

def get_user():
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            return session
        return None
    except:
        return None