import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


# ── Plans ─────────────────────────────────────────────────────────────────────

def load_plan(user_id):
    """Return the user's most recent active plan row, or None if none exists."""
    try:
        res = (
            supabase.table("plans")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None
    except Exception:
        return None


def save_plan(user_id, plan_data):
    """Delete existing plan for user then insert the new one."""
    try:
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        supabase.table("plans").insert({
            "user_id":    user_id,
            "plan_data":  plan_data,
            "start_date": plan_data["start_date"],
        }).execute()
        return True
    except Exception as e:
        raise RuntimeError(f"Supabase save_plan failed: {e}") from e


def delete_plan(user_id):
    """Delete active plan AND all session logs for this user."""
    try:
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        supabase.table("workout_logs").delete().eq("user_id", user_id).execute()
    except Exception as e:
        st.error(f"Error deleting plan: {e}")


def archive_plan(user_id, plan_data, log_data):
    """Copy current plan + log snapshot into plan_history for long-term tracking."""
    try:
        supabase.table("plan_history").insert({
            "user_id":   user_id,
            "plan_data": plan_data,
            "log_data":  log_data,
        }).execute()
    except Exception as e:
        st.error(f"Error archiving plan: {e}")


def get_plan_history(user_id):
    """Return all archived plan+log pairs for a user (used by progress dashboard)."""
    try:
        res = (
            supabase.table("plan_history")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


# ── Workout Logs ──────────────────────────────────────────────────────────────

def load_logs(user_id):
    """Return {session_id: log_row} dict for the user's current plan."""
    try:
        res = (
            supabase.table("workout_logs")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return {row["session_id"]: row for row in (res.data or [])}
    except Exception:
        return {}


def save_log_entry(user_id, session_id, entry):
    """Upsert a session log entry (insert or update depending on existence)."""
    try:
        existing = (
            supabase.table("workout_logs")
            .select("id")
            .eq("user_id", user_id)
            .eq("session_id", session_id)
            .execute()
        )
        if existing.data:
            supabase.table("workout_logs").update(entry).eq("user_id", user_id).eq("session_id", session_id).execute()
        else:
            supabase.table("workout_logs").insert({**entry, "user_id": user_id, "session_id": session_id}).execute()
    except Exception as e:
        st.error(f"Error saving session log: {e}")