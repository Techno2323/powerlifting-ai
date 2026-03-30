"""
Configuration for Powerlifting AI
"""
import streamlit as st

# Gemini API configuration (migrated from Groq)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Gemini model and generation settings
GEMINI_MODEL = "gemini-2.5-flash-lite"  # Fast, cost-effective for JSON generation
GEMINI_MAX_TOKENS = 1500
GEMINI_TEMPERATURE = 0.1  # Very low for consistent JSON output
GEMINI_TOP_P = 0.95