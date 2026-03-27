# core/exceptions.py
"""Custom exception hierarchy for powerlifting-ai."""


class PowerliftingAIError(Exception):
    """Base exception for all application errors."""


class ValidationError(PowerliftingAIError):
    """Raised when input data fails validation (email, password, user_id, etc.)."""


class AuthError(PowerliftingAIError):
    """Raised when an authentication or authorisation operation fails."""


class DatabaseError(PowerliftingAIError):
    """Raised when a database operation fails unexpectedly."""


class PlanNotFoundError(DatabaseError):
    """Raised when a requested plan does not exist for the given user."""
