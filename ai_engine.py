"""
Unified AI Engine - Gemini Integration
Handles: Training, Diet, Tips - ALL IN ONE CALL
Better JSON parsing and error handling
"""

import google.generativeai as genai
import json
import logging
from config import *
from prompts import get_unified_prompt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini lazily so a missing key only fails at generation time, not import
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info(f"✅ Gemini configured with model: {GEMINI_MODEL}")
    else:
        logger.warning("⚠️ GEMINI_API_KEY not set — AI generation will fail until it is provided.")
except Exception as e:
    logger.error(f"❌ Failed to configure Gemini: {str(e)}")
    raise


def generate_program(user_stats):
    """
    🎯 MAIN FUNCTION - Generates EVERYTHING in ONE Gemini call
    
    Args:
        user_stats (dict): {
            'squat': int,
            'bench': int,
            'deadlift': int,
            'bodyweight': int,
            'height': int,
            'age': int,
            'goal': str,
            'days': int,
            'food': str,
            'activity': str
        }
    
    Returns:
        dict: {
            'training': {...},
            'diet': {...},
            'tips': [...]
        }
    
    Raises:
        ValueError: If response is invalid
        Exception: For API errors
    """
    
    try:
        logger.info(f"🔥 Generating program for: {user_stats['bodyweight']}kg, Goal: {user_stats['goal']}")
        
        # ========== STEP 1: Generate prompt ==========
        prompt = get_unified_prompt(user_stats)
        logger.info("✅ Prompt generated")
        
        # ========== STEP 2: Call Gemini API ==========
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TEMPERATURE,
                max_output_tokens=GEMINI_MAX_TOKENS,
            )
        )
        
        logger.info("✅ Got response from Gemini")
        
        # ========== STEP 3: Parse response ==========
        # Prefer candidates[0].content.parts[0].text (Gemini SDK); fall back to response.text
        try:
            response_text = response.candidates[0].content.parts[0].text.strip()
        except (AttributeError, IndexError):
            response_text = response.text.strip()
        
        # Debug: Log first 300 chars
        logger.info(f"Response preview: {response_text[:300]}")
        
        # Strip everything before the first '{' to remove markdown / prose preamble
        brace_idx = response_text.find('{')
        if brace_idx == -1:
            logger.error(f"❌ No JSON found in response. Preview: {response_text[:500]}")
            raise ValueError("Gemini response doesn't contain valid JSON")
        
        json_text = response_text[brace_idx:]
        
        # Also strip any trailing code fence markers
        json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        logger.info(f"✅ Extracted JSON (length: {len(json_text)} chars)")
        
        # ========== STEP 4: Parse JSON ==========
        try:
            data = json.loads(json_text)
            logger.info("✅ JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON Parse Error: {str(e)}")
            logger.error(f"Problematic JSON: {json_text[:500]}")
            raise ValueError(f"Invalid JSON from Gemini: {str(e)}")
        
        # ========== STEP 5: Validate response ==========
        training_days = user_stats.get("days", 3)
        validated_data = validate_response(data, training_days=training_days)
        logger.info("✅ Response validated")
        
        return validated_data
        
    except ValueError as e:
        logger.error(f"❌ ValueError: {str(e)}")
        raise ValueError(f"Error generating program: {str(e)}")
    
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        raise Exception(f"Error generating program: {str(e)}")


def validate_response(data, training_days: int = 3):
    """
    ✅ Validate and normalize Gemini response structure.
    Ensures weeks[] -> days[] -> exercises[] hierarchy.

    Args:
        data (dict): Raw response from Gemini
        training_days (int): Number of training days per week (used for fallback)

    Returns:
        dict: Validated and normalized data
    """

    logger.info("🔍 Validating response structure...")

    if not isinstance(data, dict):
        logger.error("❌ Response is not a dictionary")
        raise ValueError("Response must be a dictionary")

    # ========== VALIDATE TRAINING ==========
    if "training" not in data or not isinstance(data.get("training"), dict):
        logger.warning("⚠️ 'training' key missing or invalid, creating default")
        data["training"] = {}

    if "weeks" not in data["training"] or not isinstance(data["training"].get("weeks"), list):
        logger.warning("⚠️ 'weeks' key missing in training")
        data["training"]["weeks"] = []

    # ========== ENSURE days[] STRUCTURE INSIDE EACH WEEK ==========
    _normalize_weeks(data["training"]["weeks"], training_days)

    # ========== VALIDATE DIET ==========
    if "diet" not in data or not isinstance(data.get("diet"), dict):
        logger.warning("⚠️ 'diet' key missing or invalid, creating default")
        data["diet"] = {}

    if "meals" not in data["diet"] or not isinstance(data["diet"].get("meals"), list):
        logger.warning("⚠️ 'meals' key missing in diet")
        data["diet"]["meals"] = []

    # ========== VALIDATE TIPS ==========
    if "tips" not in data or not isinstance(data.get("tips"), list):
        logger.warning("⚠️ 'tips' key missing or invalid, resetting")
        data["tips"] = []

    default_tips = [
        "Stay consistent with your training schedule.",
        "Track your progress weekly and adjust intensity as needed.",
        "Prioritize proper form over heavy weight.",
        "Get adequate sleep for recovery.",
        "Listen to your body and take rest days when needed.",
    ]
    while len(data["tips"]) < 5:
        data["tips"].append(default_tips[len(data["tips"])])

    # ========== VALIDATE DIET NUMBERS ==========
    for key in ["calories", "protein", "carbs", "fats", "maintenance", "tdee"]:
        if key not in data["diet"]:
            logger.warning(f"⚠️ Diet missing '{key}', setting to 0")
            data["diet"][key] = 0

    total_days = sum(len(w.get("days", [])) for w in data["training"]["weeks"])
    logger.info(
        "✅ Validation complete: weeks=%d total_days=%d diet_meals=%d tips=%d",
        len(data["training"]["weeks"]),
        total_days,
        len(data["diet"]["meals"]),
        len(data["tips"]),
    )

    return data


def _normalize_weeks(weeks: list, training_days: int) -> None:
    """
    Ensure every week in *weeks* has a proper days[] -> exercises[] structure.
    If a week has a flat 'exercises' list instead of 'days', the exercises are
    distributed evenly across *training_days* synthetic days.
    If a week already has days but some are empty, fallback exercises are added.
    """
    _fallback_exercises = [
        {"name": "Back Squat",   "sets": 3, "reps": "5", "weight": 60,  "rpe": 6, "note": "Focus on depth and bracing"},
        {"name": "Bench Press",  "sets": 3, "reps": "5", "weight": 50,  "rpe": 6, "note": "Retract shoulder blades"},
        {"name": "Deadlift",     "sets": 3, "reps": "5", "weight": 80,  "rpe": 6, "note": "Neutral spine throughout"},
        {"name": "Leg Press",    "sets": 3, "reps": "8", "weight": 100, "rpe": 6, "note": "Full range of motion"},
        {"name": "Dumbbell Row", "sets": 3, "reps": "8", "weight": 20,  "rpe": 6, "note": "Control the eccentric"},
    ]

    for idx, week in enumerate(weeks):
        if not isinstance(week, dict):
            logger.warning("⚠️ Week %d is not a dict, skipping", idx + 1)
            continue

        days_list = week.get("days")

        # Case 1: flat exercises[] instead of days[] — distribute across days
        if not isinstance(days_list, list) or not days_list:
            flat_exercises = week.get("exercises")
            if isinstance(flat_exercises, list) and flat_exercises:
                logger.warning(
                    "⚠️ Week %d has flat exercises[]. Distributing %d exercises across %d days.",
                    week.get("week", idx + 1), len(flat_exercises), training_days,
                )
                days_list = _distribute_exercises(flat_exercises, training_days, week.get("week", idx + 1))
            else:
                logger.warning(
                    "⚠️ Week %d has no days[] and no exercises[]. Creating %d fallback days.",
                    week.get("week", idx + 1), training_days,
                )
                days_list = _make_fallback_days(_fallback_exercises, training_days, week.get("week", idx + 1))

            week["days"] = days_list
            week.pop("exercises", None)

        # Case 2: days exist but some are empty or missing exercises
        for day in days_list:
            if not isinstance(day, dict):
                continue
            if not isinstance(day.get("exercises"), list) or not day["exercises"]:
                logger.warning(
                    "⚠️ Week %d Day %s has no exercises. Adding fallback.",
                    week.get("week", idx + 1), day.get("day_number", "?"),
                )
                day["exercises"] = list(_fallback_exercises[:4])

        # Ensure day_number is present on every day
        for d_idx, day in enumerate(days_list, 1):
            if isinstance(day, dict) and "day_number" not in day:
                day["day_number"] = d_idx

        week["days"] = days_list


def _distribute_exercises(exercises: list, training_days: int, week_num: int) -> list:
    """Split a flat exercises list into *training_days* day buckets."""
    days = []
    per_day = max(1, len(exercises) // training_days)
    for d in range(training_days):
        start = d * per_day
        end = start + per_day if d < training_days - 1 else len(exercises)
        day_exercises = exercises[start:end]
        # If this bucket is empty (can happen when len(exercises) < training_days),
        # cycle through the exercise list rather than repeating the same first 4.
        if not day_exercises:
            day_exercises = [exercises[d % len(exercises)]]
        days.append({
            "day_number": d + 1,
            "label": f"Day {d + 1}",
            "exercises": day_exercises,
        })
    return days


def _make_fallback_days(fallback_exercises: list, training_days: int, week_num: int) -> list:
    """Create *training_days* days each loaded with fallback exercises."""
    return [
        {
            "day_number": d + 1,
            "label": f"Day {d + 1}",
            "exercises": list(fallback_exercises[:4]),
        }
        for d in range(training_days)
    ]


def calculate_weak_point(squat, bench, deadlift, bodyweight):
    """
    Calculate athlete's weak point based on lift ratios
    
    Args:
        squat, bench, deadlift, bodyweight: integers (kg)
    
    Returns:
        str: "bench", "squat", or "balanced"
    """
    
    if bodyweight <= 0:
        return "balanced"
    
    bench_ratio = bench / bodyweight
    squat_dl_ratio = squat / deadlift if deadlift > 0 else 1.0
    
    logger.info(f"Weak point analysis: Bench/BW={bench_ratio:.2f}, Squat/DL={squat_dl_ratio:.2f}")
    
    if bench_ratio < BENCH_RATIO_THRESHOLD:
        logger.info("→ Weak point: BENCH")
        return "bench"
    elif squat_dl_ratio < SQUAT_DL_RATIO_THRESHOLD:
        logger.info("→ Weak point: SQUAT")
        return "squat"
    else:
        logger.info("→ Weak point: BALANCED")
        return "balanced"


def calculate_macros(bodyweight, height, age, goal, activity):
    """
    Calculate nutritional targets
    
    Args:
        bodyweight: int (kg)
        height: int (cm)
        age: int (years)
        goal: str ("Build Strength", "Powerbuilding", "Bulk", "Cut")
        activity: str ("Sedentary", "Light", "Moderate", "Very Active")
    
    Returns:
        dict: {calories, protein, carbs, fats, maintenance, tdee}
    """
    
    try:
        # Mifflin-St Jeor equation for maintenance
        maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
        logger.info(f"Maintenance: {int(maintenance)} kcal")
        
        # Calculate TDEE
        activity_mult = ACTIVITY_MULTIPLIERS.get(activity, 1.55)
        tdee = maintenance * activity_mult
        logger.info(f"TDEE ({activity}): {int(tdee)} kcal")
        
        # Goal-specific calories and macros
        if goal == "Build Strength":
            calories = int(tdee + CALORIE_SURPLUS_STRENGTH)
            protein = int(bodyweight * PROTEIN_RATIO)
            carbs = int(bodyweight * CARBS_RATIO)
            fats = int(bodyweight * FATS_RATIO)
        
        elif goal == "Powerbuilding":
            calories = int(tdee + CALORIE_SURPLUS_POWERBUILDING)
            protein = int(bodyweight * POWERBUILDING_PROTEIN_RATIO)
            carbs = int(bodyweight * POWERBUILDING_CARBS_RATIO)
            fats = int(bodyweight * POWERBUILDING_FATS_RATIO)
        
        elif goal == "Bulk":
            calories = int(tdee + CALORIE_SURPLUS_BULK)
            protein = int(bodyweight * PROTEIN_RATIO)
            carbs = int(bodyweight * CARBS_RATIO)
            fats = int(bodyweight * FATS_RATIO)
        
        else:  # Cut
            calories = int(tdee - CALORIE_DEFICIT_CUT)
            protein = int(bodyweight * PROTEIN_RATIO)
            carbs = int(bodyweight * CARBS_RATIO)
            fats = int(bodyweight * FATS_RATIO)
        
        logger.info(f"Macros - Protein: {protein}g, Carbs: {carbs}g, Fats: {fats}g, Calories: {calories}")
        
        return {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "maintenance": int(maintenance),
            "tdee": int(tdee)
        }
    
    except Exception as e:
        logger.error(f"❌ Error calculating macros: {str(e)}")
        raise


def format_response_for_display(program_data):
    """
    Format response for nice display in Streamlit
    
    Args:
        program_data (dict): Raw program data from Gemini
    
    Returns:
        dict: Formatted for display
    """
    
    formatted = {
        "summary": program_data.get("training", {}).get("summary", "Program generated"),
        "training": {
            "weeks": len(program_data.get("training", {}).get("weeks", []))
        },
        "diet": {
            "calories": program_data.get("diet", {}).get("calories", 0),
            "protein": program_data.get("diet", {}).get("protein", 0),
            "carbs": program_data.get("diet", {}).get("carbs", 0),
            "fats": program_data.get("diet", {}).get("fats", 0),
            "meals": len(program_data.get("diet", {}).get("meals", []))
        },
        "tips": len(program_data.get("tips", []))
    }
    
    return formatted


def log_program_summary(program_data, user_stats):
    """
    Log a summary of generated program
    
    Args:
        program_data (dict): Generated program
        user_stats (dict): User input stats
    """
    
    logger.info("=" * 60)
    logger.info("📊 PROGRAM GENERATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Athlete: {user_stats['age']}yo, {user_stats['bodyweight']}kg")
    logger.info(f"Lifts: S{user_stats['squat']}kg B{user_stats['bench']}kg D{user_stats['deadlift']}kg")
    logger.info(f"Goal: {user_stats['goal']}")
    logger.info(f"Training: {user_stats['days']} days/week")
    logger.info(f"Diet: {user_stats['food']}, {user_stats['activity']}")
    logger.info("-" * 60)
    logger.info(f"Training weeks: {len(program_data.get('training', {}).get('weeks', []))}")
    logger.info(f"Diet meals: {len(program_data.get('diet', {}).get('meals', []))}")
    logger.info(f"Coaching tips: {len(program_data.get('tips', []))}")
    logger.info(f"Calories: {program_data.get('diet', {}).get('calories', 'N/A')} kcal")
    logger.info(f"Protein: {program_data.get('diet', {}).get('protein', 'N/A')}g")
    logger.info("=" * 60)