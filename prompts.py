"""
Powerlifting AI Coach - Gemini 2.5 Flash Lite Optimized Minimal Prompt
"""

def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, goal, days, food, activity):
    """Generate minimal JSON to avoid truncation on Gemini 2.5 Flash Lite."""
    
    # Calculate maintenance calories
    maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
    
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
    
    bench_ratio = bench / bodyweight
    squat_dl_ratio = squat / deadlift if deadlift > 0 else 1
    
    if bench_ratio < 1.3:
        weak_point = "bench"
    elif squat_dl_ratio < 0.75:
        weak_point = "squat"
    else:
        weak_point = "balanced"

    # ULTRA-MINIMAL prompt for Gemini 2.5 Flash Lite
    prompt = f"""Design a {days}-day powerlifting program (4 weeks).

ATHLETE: Squat {squat}kg, Bench {bench}kg, DL {deadlift}kg, BW {bodyweight}kg, Age {age}
WEAK: {weak_point} | GOAL: {goal} | DIET: {food}
TDEE: {int(tdee)}kcal, TARGET: {calories}kcal, P: {protein}g, C: {carbs}g, F: {fats}g

Return ONLY this JSON (no markdown, no extra text):
{{
  "weeks": [
    {{"week": 1, "focus": "Accumulation", "days": [{{"day_number": 1, "label": "Squat Focus", "exercises": [{{"name": "Squat", "sets": 4, "reps": 8, "weight": {int(squat*0.73)}, "rpe": 7}}]}}]}},
    {{"week": 2, "focus": "Intensification", "days": [{{"day_number": 1, "label": "Bench Focus", "exercises": [{{"name": "Bench Press", "sets": 4, "reps": 6, "weight": {int(bench*0.78)}, "rpe": 8}}]}}]}},
    {{"week": 3, "focus": "Peak", "days": [{{"day_number": 1, "label": "Deadlift Focus", "exercises": [{{"name": "Deadlift", "sets": 3, "reps": 3, "weight": {int(deadlift*0.85)}, "rpe": 9}}]}}]}},
    {{"week": 4, "focus": "Deload", "days": [{{"day_number": 1, "label": "Recovery", "exercises": [{{"name": "Light Squat", "sets": 2, "reps": 5, "weight": {int(squat*0.50)}, "rpe": 5}}]}}]}}
  ],
  "diet": {{"calories": {calories}, "protein": {protein}, "carbs": {carbs}, "fats": {fats}}},
  "tips": ["Progressive overload builds strength", "Rest 2-3 min between heavy sets", "Form over ego"]
}}"""

    return prompt