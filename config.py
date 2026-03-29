"""
Configuration for Powerlifting AI
"""
import streamlit as st

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except:
    GROQ_API_KEY = ""

USE_GROQ = True

# Using 70B versatile model - can handle more tokens
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS = 6000  # Increased for better quality
GROQ_TEMPERATURE = 0.2  # Low temp for consistent JSON