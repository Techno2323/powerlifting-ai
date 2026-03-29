"""
Unified AI Engine - Gemini Integration
Handles: Training, Diet, Tips - ALL IN ONE CALL
Better JSON parsing and error handling
"""

import google.generativeai as genai
import json
import re
import logging
from config import *
from prompts import get_unified_prompt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info(f"✅ Gemini configured with model: {GEMINI_MODEL}")
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
        response_text = response.text.strip()
        
        # Debug: Log first 300 chars
        logger.info(f"Response preview: {response_text[:300]}")
        
        # Try to extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        
        if not json_match:
            logger.error(f"❌ No JSON found in response")
            logger.error(f"Full response: {response_text}")
            raise ValueError("Gemini response doesn't contain valid JSON")
        
        json_text = json_match.group()
        
        # Clean up common issues
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
        validated_data = validate_response(data)
        logger.info("✅ Response validated")
        
        return validated_data
        
    except ValueError as e:
        logger.error(f"❌ ValueError: {str(e)}")
        raise ValueError(f"Error generating program: {str(e)}")
    
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        raise Exception(f"Error generating program: {str(e)}")


def validate_response(data):
    """
    ✅ Validate and normalize Gemini response structure
    
    Args:
        data (dict): Raw response from Gemini
    
    Returns:
        dict: Validated and normalized data
    """
    
    logger.info("🔍 Validating response structure...")
    
    if not isinstance(data, dict):
        logger.error("❌ Response is not a dictionary")
        raise ValueError("Response must be a dictionary")
    
    # ========== VALIDATE TRAINING ==========
    if "training" not in data:
        logger.warning("⚠️ 'training' key missing, creating default")
        data["training"] = {}
    
    if not isinstance(data.get("training"), dict):
        logger.warning("⚠️ 'training' is not dict, resetting")
        data["training"] = {}
    
    # Ensure training has weeks
    if "weeks" not in data.get("training", {}):
        logger.warning("⚠️ 'weeks' key missing in training")
        data["training"]["weeks"] = []
    
    # ========== VALIDATE DIET ==========
    if "diet" not in data:
        logger.warning("⚠️ 'diet' key missing, creating default")
        data["diet"] = {}
    
    if not isinstance(data.get("diet"), dict):
        logger.warning("⚠️ 'diet' is not dict, resetting")
        data["diet"] = {}
    
    # Ensure diet has meals
    if "meals" not in data.get("diet", {}):
        logger.warning("⚠️ 'meals' key missing in diet")
        data["diet"]["meals"] = []
    
    # ========== VALIDATE TIPS ==========
    if "tips" not in data:
        logger.warning("⚠️ 'tips' key missing, creating default")
        data["tips"] = []
    
    if not isinstance(data.get("tips"), list):
        logger.warning("⚠️ 'tips' is not list, resetting")
        data["tips"] = []
    
    # Ensure we have at least 5 tips
    if len(data["tips"]) < 5:
        logger.warning(f"⚠️ Only {len(data['tips'])} tips, filling to 5")
        default_tips = [
            "Stay consistent with your training schedule.",
            "Track your progress weekly and adjust intensity as needed.",
            "Prioritize proper form over heavy weight.",
            "Get adequate sleep for recovery.",
            "Listen to your body and take rest days when needed."
        ]
        while len(data["tips"]) < 5:
            data["tips"].append(default_tips[len(data["tips"])])
    
    # ========== VALIDATE DIET NUMBERS ==========
    diet_keys = ["calories", "protein", "carbs", "fats", "maintenance", "tdee"]
    for key in diet_keys:
        if key not in data.get("diet", {}):
            logger.warning(f"⚠️ Diet missing '{key}', setting to 0")
            if "diet" not in data:
                data["diet"] = {}
            data["diet"][key] = 0
    
    logger.info(f"✅ Validation complete:")
    logger.info(f"   - Training weeks: {len(data.get('training', {}).get('weeks', []))}")
    logger.info(f"   - Diet meals: {len(data.get('diet', {}).get('meals', []))}")
    logger.info(f"   - Tips: {len(data.get('tips', []))}")
    
    return data


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