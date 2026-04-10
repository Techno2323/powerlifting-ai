"""
Configuration for Powerlifting AI
"""
import streamlit as st

try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except:
    GEMINI_API_KEY = ""

USE_GEMINI = True

# Using gemini-3.1-flash-lite-preview as requested to fix token limits
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
GEMINI_MAX_TOKENS = 8192  # Increased for larger responses
GEMINI_TEMPERATURE = 0.65  # Higher for personalization; prompt constraints keep JSON intact