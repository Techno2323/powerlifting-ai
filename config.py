"""
Unified Configuration for Powerlifting AI
All settings in one place - easy to manage
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========== GEMINI API CONFIG ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")  # ✅ FIXED
GEMINI_MAX_TOKENS = 2000
GEMINI_TEMPERATURE = 0.7

# ========== SUPABASE CONFIG ==========
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ========== ENVIRONMENT ==========
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False") == "True"

# ========== TRAINING CONSTANTS ==========
TRAINING_WEEKS = 4
MIN_TRAINING_DAYS = 3
MAX_TRAINING_DAYS = 6
TRAINING_INTENSITIES = {
    "week_1": {"intensity": "70-75%", "volume": "high", "rpe": "6-7"},
    "week_2": {"intensity": "75-80%", "volume": "moderate", "rpe": "7-8"},
    "week_3": {"intensity": "82-87%", "volume": "low", "rpe": "8-9"},
    "week_4": {"intensity": "60-65%", "volume": "high", "rpe": "5-6"}
}

# ========== DIET CONSTANTS ==========
MEAL_SLOTS = 6
DIET_TYPES = ["Vegetarian", "Non-Vegetarian", "Eggetarian"]
GOALS = ["Build Strength", "Powerbuilding", "Bulk", "Cut"]
ACTIVITY_LEVELS = ["Sedentary", "Light", "Moderate", "Very Active"]



# ========== CALORIE SETTINGS ==========
CALORIE_SURPLUS_STRENGTH = 300  # kcal
CALORIE_SURPLUS_BULK = 500      # kcal
CALORIE_DEFICIT_CUT = 500       # kcal

# ========== POWERBUILDING SPECIFIC ==========
CALORIE_SURPLUS_POWERBUILDING = 400  # kcal (between strength & bulk)
POWERBUILDING_PROTEIN_RATIO = 2.4    # g per kg (slightly higher for muscle)
POWERBUILDING_CARBS_RATIO = 5.8      # g per kg (slightly higher for volume)
POWERBUILDING_FATS_RATIO = 1.0       # g per kg (slightly lower)

# ========== MACRO RATIOS ==========
PROTEIN_RATIO = 2.2   # g per kg bodyweight
CARBS_RATIO = 5.5     # g per kg bodyweight
FATS_RATIO = 1.1      # g per kg bodyweight

# ========== ACTIVITY MULTIPLIERS (TDEE Calculation) ==========
ACTIVITY_MULTIPLIERS = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Very Active": 1.725
}

# ========== WEAK POINT THRESHOLDS ==========
BENCH_RATIO_THRESHOLD = 1.3  # If bench/BW < 1.3, weak point = bench
SQUAT_DL_RATIO_THRESHOLD = 0.75  # If squat/DL < 0.75, weak point = squat

# ========== VALIDATION ==========
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE credentials not found in .env file!")