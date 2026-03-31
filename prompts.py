"""
Powerlifting AI Coach - Dynamic Gemini Prompt
"""
import json

def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, gender, goal, days, food, activity, target_week=1):
    """Generate training program - Dynamic JSON for Gemini"""
    
    # Calculate maintenance calories
    # Mifflin-St Jeor equation factoring in gender
    if gender.lower() == "male":
        maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
    else:
        maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) - 161
        
    activity_multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Very Active": 1.725}
    tdee = maintenance * activity_multipliers.get(activity, 1.55)
    
    if goal == "Build Strength":
        calories = int(tdee + 300)
    elif goal == "Bulk":
        calories = int(tdee + 500)
    else:
        calories = int(tdee - 500)
    
    protein = int(bodyweight * 2.2)
    carbs = int(bodyweight * 5.5)
    fats = int(bodyweight * 1.1)
    
    # Calculate ratios to identify weak points (can be overridden by AI)
    bench_ratio = bench / bodyweight
    squat_dl_ratio = squat / deadlift if deadlift > 0 else 1.0
    
    weak_point = "balanced"
    if bench_ratio < 1.3 and gender.lower() == "male":
        weak_point = "bench"
    elif bench_ratio < 0.8 and gender.lower() == "female":
        weak_point = "bench"
    if target_week == 1:
        json_schema = f"""JSON SCHEMA REQUIREMENTS (OUTPUT AS MARKDOWN BACKTICKS ```json ... ```):
- Root object must contain: "summary" (string), "goal" (string), "training_days" (integer), "weak_point" (string), "week" (integer 1), "focus" (string), "diet" (object), "tips" (array of exactly 3 strings), and keys for each training day: "day1_ex", "day2_ex" ... up to "day{days}_ex".
- Each "dayX_ex" must be an array of exercise objects.
- Each exercise object must contain: "name" (string), "sets" (integer), "reps" (string), "weight" (integer representing kg), "rpe" (integer).
- The "diet" object must contain: "calories": {calories}, "protein": {protein}, "carbs": {carbs}, "fats": {fats}, "maintenance": {int(maintenance)}, "tdee": {int(tdee)}.

CRITICAL: Return ONLY Week 1 metrics and the global summary/diet. Do NOT return all 4 weeks. Ensure exercises are tailored for Week 1 (Volume Accumulation)."""
    else:
        json_schema = f"""JSON SCHEMA REQUIREMENTS (OUTPUT AS MARKDOWN BACKTICKS ```json ... ```):
- Root object must contain: "week" (integer {target_week}), "focus" (string), and keys for each training day: "day1_ex", "day2_ex" ... up to "day{days}_ex".
- Each "dayX_ex" must be an array of exercise objects.
- Each exercise object must contain: "name" (string), "sets" (integer), "reps" (string), "weight" (integer representing kg), "rpe" (integer).

CRITICAL: Return ONLY Week {target_week}. Do NOT return all 4 weeks. Ensure exercises are tailored for Week {target_week} of a typical powerlifting block."""

    prompt = f"""You are an elite Powerlifting AI Coach. Your task is to design Week {target_week} of a highly personalized, dynamic 4-week {days}-day training program for my client. 

Do NOT just return a generic template. You must carefully consider the athlete's age, gender, bodyweight, and current strength levels when selecting exercises, calculating weights, and planning volume. Keep exercise names very concise (e.g. "Squat", not "High Bar Back Squat with pause").

ATHLETE PROFILE:
- Gender: {gender}
- Age: {age} years old
- Bodyweight: {bodyweight} kg
- Height: {height} cm
- Experience Level Indicators: Squat {squat}kg, Bench {bench}kg, Deadlift {deadlift}kg
- Identified Weak Point: {weak_point}
- Training Goal: {goal}
- Training Frequency: {days} days/week

YOUR INSTRUCTIONS:
1. Act as a world-class coach. Empathize with an athlete who is a {age}-year-old {gender} weighing {bodyweight}kg. Their recovery needs, exercise selection (e.g., using variations like paused work, DB work, mobility drills) and rep schemes MUST be customized to them.
2. If the athlete is lighter or older, adjust the absolute volume and intensity to prevent injury, perhaps adding more prehab/mobility work or accessory variations rather than just heavy barbell lifts.
3. Calculate specific weights (in kg) for all main working sets based on their provided maxes ({squat}kg/{bench}kg/{deadlift}kg) and the phase (Week 1 volume, Week 3 peaking, etc.).
4. Include specific assistance and accessory exercises that target their {weak_point} weak point.
5. CRITICAL: Vary the number of exercises per day realistically! A brutal, heavy Deadlift or Squat day should only contain 3 to 4 exercises total due to severe CNS fatigue. A lighter Bench or localized Hypertrophy accessory day should contain 5 to 6 exercises. Do NOT make every single day the exact same length.
6. Provide actionable, personalized "tips" at the end.

You MUST return ONLY a valid JSON object matching exactly the rules below. Do NOT include markdown blocks formatting (no ```json).

{json_schema}
"""
    return prompt