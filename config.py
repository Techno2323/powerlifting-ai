"""
Configuration for Powerlifting AI - Gemini 2.5 Flash Lite Optimized
"""
import streamlit as st

# Gemini API configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# **CRITICAL**: Gemini 2.5 Flash Lite model settings
GEMINI_MODEL = "gemini-2.5-flash-lite"
GEMINI_MAX_TOKENS = 1024  # Reduced from 6000 to prevent truncation
GEMINI_TEMPERATURE = 0.05  # Very low for consistent JSON
GEMINI_TOP_P = 0.9