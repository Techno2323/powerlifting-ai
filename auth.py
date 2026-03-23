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
        res = supabase.auth.get_user()
        if res and res.user:
            return res
        return None
    except:
        return None