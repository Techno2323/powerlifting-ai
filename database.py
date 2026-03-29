import logging
import streamlit as st
from supabase import create_client
from core.exceptions import DatabaseError, ValidationError

logger = logging.getLogger(__name__)

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


# ── Shared validation helper ──────────────────────────────────────────────────

def _require_user_id(user_id) -> None:
    """Raise ValidationError if *user_id* is falsy or not a string."""
    if not user_id or not isinstance(user_id, str):
        raise ValidationError("user_id must be a non-empty string.")


# ── Plan Repository ───────────────────────────────────────────────────────────

class PlanRepository:
    """Handles all database operations for training plans."""

    def load(self, user_id: str):
        """Return the user's most recent active plan row, or None if none exists."""
        _require_user_id(user_id)
        try:
            res = (
                supabase.table("plans")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            plan = res.data[0] if res.data else None
            logger.debug("load_plan for user %s: found=%s", user_id, plan is not None)
            return plan
        except Exception as exc:
            logger.error("load_plan failed for user %s: %s", user_id, exc)
            return None

    def save(self, user_id: str, plan_data: dict) -> bool:
        """Delete existing plan for user then insert the new one."""
        _require_user_id(user_id)
        if not isinstance(plan_data, dict):
            raise ValidationError("plan_data must be a dictionary.")

        # Log structure for debugging
        self._log_plan_structure(user_id, plan_data)

        try:
            supabase.table("plans").delete().eq("user_id", user_id).execute()
            supabase.table("plans").insert({
                "user_id":    user_id,
                "plan_data":  plan_data,
                "start_date": plan_data["start_date"],
            }).execute()
            logger.info("save_plan succeeded for user %s", user_id)
            return True
        except Exception as exc:
            logger.error("save_plan failed for user %s: %s", user_id, exc)
            raise DatabaseError(f"save_plan failed: {exc}") from exc

    @staticmethod
    def _log_plan_structure(user_id: str, plan_data: dict) -> None:
        """Log the week/day/exercise structure of the plan for debugging."""
        try:
            training = plan_data.get("training", {})
            weeks = training.get("weeks", []) if isinstance(training, dict) else []
            has_days = all(
                isinstance(w.get("days"), list) and len(w.get("days", [])) > 0
                for w in weeks
                if isinstance(w, dict)
            )
            total_days = sum(
                len(w.get("days", []))
                for w in weeks
                if isinstance(w, dict)
            )
            total_exercises = sum(
                len(d.get("exercises", []))
                for w in weeks if isinstance(w, dict)
                for d in w.get("days", []) if isinstance(d, dict)
            )
            if not has_days:
                logger.warning(
                    "save_plan for user %s: plan missing days[] in some weeks — "
                    "dashboard may not display correctly", user_id
                )
            else:
                logger.info(
                    "save_plan for user %s: structure OK — %d weeks, %d days, %d exercises",
                    user_id, len(weeks), total_days, total_exercises,
                )
        except Exception as exc:  # pragma: no cover
            logger.warning("save_plan structure check failed for user %s: %s", user_id, exc)

    def delete(self, user_id: str) -> None:
        """Delete active plan AND all session logs for this user."""
        _require_user_id(user_id)
        try:
            supabase.table("plans").delete().eq("user_id", user_id).execute()
            supabase.table("workout_logs").delete().eq("user_id", user_id).execute()
            logger.info("delete_plan succeeded for user %s", user_id)
        except Exception as exc:
            logger.error("delete_plan failed for user %s: %s", user_id, exc)
            raise DatabaseError(f"delete_plan failed: {exc}") from exc

    def archive(self, user_id: str, plan_data: dict, log_data: dict) -> None:
        """Copy current plan + log snapshot into plan_history for long-term tracking."""
        _require_user_id(user_id)
        try:
            supabase.table("plan_history").insert({
                "user_id":   user_id,
                "plan_data": plan_data,
                "log_data":  log_data,
            }).execute()
            logger.info("archive_plan succeeded for user %s", user_id)
        except Exception as exc:
            logger.error("archive_plan failed for user %s: %s", user_id, exc)
            raise DatabaseError(f"archive_plan failed: {exc}") from exc

    def get_history(self, user_id: str) -> list:
        """Return all archived plan+log pairs for a user (used by progress dashboard)."""
        _require_user_id(user_id)
        try:
            res = (
                supabase.table("plan_history")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return res.data or []
        except Exception as exc:
            logger.error("get_plan_history failed for user %s: %s", user_id, exc)
            return []


# ── Workout Log Repository ────────────────────────────────────────────────────

class WorkoutRepository:
    """Handles all database operations for workout logs."""

    def load_logs(self, user_id: str) -> dict:
        """Return {session_id: log_row} dict for the user's current plan."""
        _require_user_id(user_id)
        try:
            res = (
                supabase.table("workout_logs")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            logs = {row["session_id"]: row for row in (res.data or [])}
            logger.debug("load_logs for user %s: %d entries", user_id, len(logs))
            return logs
        except Exception as exc:
            logger.error("load_logs failed for user %s: %s", user_id, exc)
            return {}

    def save_log_entry(self, user_id: str, session_id: str, entry: dict) -> None:
        """Upsert a session log entry (insert or update depending on existence)."""
        _require_user_id(user_id)
        if not session_id or not isinstance(session_id, str):
            raise ValidationError("session_id must be a non-empty string.")
        if not isinstance(entry, dict):
            raise ValidationError("entry must be a dictionary.")
        try:
            existing = (
                supabase.table("workout_logs")
                .select("id")
                .eq("user_id", user_id)
                .eq("session_id", session_id)
                .execute()
            )
            if existing.data:
                (
                    supabase.table("workout_logs")
                    .update(entry)
                    .eq("user_id", user_id)
                    .eq("session_id", session_id)
                    .execute()
                )
            else:
                supabase.table("workout_logs").insert(
                    {**entry, "user_id": user_id, "session_id": session_id}
                ).execute()
            logger.info("save_log_entry succeeded for user %s session %s", user_id, session_id)
        except Exception as exc:
            logger.error("save_log_entry failed for user %s session %s: %s", user_id, session_id, exc)
            raise DatabaseError(f"save_log_entry failed: {exc}") from exc


# ── Module-level singletons ───────────────────────────────────────────────────

_plan_repo = PlanRepository()
_workout_repo = WorkoutRepository()


# ── Backward-compatible module-level functions ────────────────────────────────

def load_plan(user_id: str):
    return _plan_repo.load(user_id)


def save_plan(user_id: str, plan_data: dict) -> bool:
    return _plan_repo.save(user_id, plan_data)


def delete_plan(user_id: str) -> None:
    _plan_repo.delete(user_id)


def archive_plan(user_id: str, plan_data: dict, log_data: dict) -> None:
    _plan_repo.archive(user_id, plan_data, log_data)


def get_plan_history(user_id: str) -> list:
    return _plan_repo.get_history(user_id)


def load_logs(user_id: str) -> dict:
    return _workout_repo.load_logs(user_id)


def save_log_entry(user_id: str, session_id: str, entry: dict) -> None:
    _workout_repo.save_log_entry(user_id, session_id, entry)