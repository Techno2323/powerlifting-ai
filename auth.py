# auth.py
import logging
import re
import streamlit as st
from database import supabase
from core.exceptions import AuthError, ValidationError

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthManager:
    """Class-based authentication manager with input validation and logging."""

    # ── Validation helpers ────────────────────────────────────────────────────

    @staticmethod
    def _validate_email(email: str) -> None:
        if not email or not isinstance(email, str):
            raise ValidationError("Email must be a non-empty string.")
        if not _EMAIL_RE.match(email.strip()):
            raise ValidationError(f"Invalid email format: {email!r}")

    @staticmethod
    def _validate_password(password: str) -> None:
        if not password or not isinstance(password, str):
            raise ValidationError("Password must be a non-empty string.")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        if not any(ch.isdigit() for ch in password):
            raise ValidationError("Password must contain at least one digit.")

    # ── Auth operations ───────────────────────────────────────────────────────

    def sign_up(self, email: str, password: str):
        """Register a new user.  Returns (response, None) or (None, error_msg)."""
        try:
            self._validate_email(email)
            self._validate_password(password)
            res = supabase.auth.sign_up({"email": email.strip(), "password": password})
            logger.info("sign_up succeeded for %s", email)
            return res, None
        except ValidationError as exc:
            logger.warning("sign_up validation error: %s", exc)
            return None, str(exc)
        except Exception as exc:
            logger.error("sign_up failed for %s: %s", email, exc)
            return None, str(exc)

    def sign_in(self, email: str, password: str):
        """Authenticate an existing user.  Stores JWT in session_state on success."""
        try:
            self._validate_email(email)
            if not password:
                raise ValidationError("Password must not be empty.")
            res = supabase.auth.sign_in_with_password(
                {"email": email.strip(), "password": password}
            )
            # 🔑 CRITICAL: Store JWT in session_state, not in the shared client
            if res and res.session:
                st.session_state["_access_token"] = res.session.access_token
                st.session_state["_refresh_token"] = res.session.refresh_token
            logger.info("sign_in succeeded for %s", email)
            return res, None
        except ValidationError as exc:
            logger.warning("sign_in validation error: %s", exc)
            return None, str(exc)
        except Exception as exc:
            logger.error("sign_in failed for %s: %s", email, exc)
            return None, str(exc)

    def sign_out(self) -> None:
        """Sign the current user out and clear all session state."""
        try:
            supabase.auth.sign_out()
            logger.info("sign_out succeeded")
        except Exception as exc:
            logger.warning("sign_out encountered an error (ignored): %s", exc)
        st.session_state.clear()
        st.rerun()

    def get_user(self):
        """Return the currently authenticated user object, or None."""
        try:
            return supabase.auth.get_user()
        except Exception as exc:
            logger.warning("get_user failed: %s", exc)
            return None


# ── Module-level singleton and backward-compatible functions ──────────────────

_auth_manager = AuthManager()


def sign_up(email: str, password: str):
    return _auth_manager.sign_up(email, password)


def sign_in(email: str, password: str):
    return _auth_manager.sign_in(email, password)


def sign_out() -> None:
    _auth_manager.sign_out()


def get_user():
    return _auth_manager.get_user()