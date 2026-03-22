import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_plan(user_id):
    try:
        res = supabase.table("plans").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        if res.data:
            return res.data[0]
        return None
    except:
        return None

def save_plan(user_id, plan_data):
    try:
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        supabase.table("plans").insert({
            "user_id": user_id,
            "plan_data": plan_data,
            "start_date": plan_data["start_date"]
        }).execute()
        return True
    except Exception as e:
        raise Exception(f"Supabase save failed: {e}")

def load_logs(user_id):
    try:
        res = supabase.table("workout_logs").select("*").eq("user_id", user_id).execute()
        return {row["session_id"]: row for row in res.data}
    except:
        return {}

def save_log_entry(user_id, session_id, entry):
    try:
        existing = supabase.table("workout_logs").select("id").eq("user_id", user_id).eq("session_id", session_id).execute()
        if existing.data:
            supabase.table("workout_logs").update(entry).eq("user_id", user_id).eq("session_id", session_id).execute()
        else:
            entry["user_id"] = user_id
            entry["session_id"] = session_id
            supabase.table("workout_logs").insert(entry).execute()
    except Exception as e:
        st.error(f"Error saving log: {e}")

def archive_plan(user_id, plan_data, log_data):
    try:
        supabase.table("plan_history").insert({
            "user_id": user_id,
            "plan_data": plan_data,
            "log_data": log_data
        }).execute()
    except Exception as e:
        st.error(f"Error archiving: {e}")

def delete_plan(user_id):
    try:
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        supabase.table("workout_logs").delete().eq("user_id", user_id).execute()
    except Exception as e:
        st.error(f"Error deleting plan: {e}")