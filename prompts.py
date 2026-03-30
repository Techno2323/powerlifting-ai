"""
Powerlifting AI Coach - Gemini Prompt (JSON-only output)
"""

def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, goal, days, food, activity):
    """Generate training program with strict JSON-only output."""
    
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
    squat_dl_ratio = squat / deadlift
    
    if bench_ratio < 1.3:
        weak_point = "bench"
    elif squat_dl_ratio < 0.75:
        weak_point = "squat"
    else:
        weak_point = "balanced"

    prompt = f"""You are a powerlifting coach. Design a 4-week {days}-day program.

ATHLETE: Squat {squat}kg, Bench {bench}kg, Deadlift {deadlift}kg, BW {bodyweight}kg, Age {age}, Height {height}cm
WEAK POINT: {weak_point}
GOAL: {goal}
TDEE: {int(tdee)} kcal, TARGET: {calories} kcal, PROTEIN: {protein}g, CARBS: {carbs}g, FATS: {fats}g

TRAINING STRUCTURE (4 weeks, {days} days per week):
Week 1: 70-75% intensity, high volume, RPE 6-7
Week 2: 75-80% intensity, moderate volume, RPE 7-8
Week 3: 82-87% intensity, low volume, RPE 8-9
Week 4: 60-65% intensity, high volume, RPE 5-6 (deload)

STRATEGY: Vary day order each week. Include recovery days. Make it coaching advice, not a template.

MAIN LIFTS BY WEEK:
Week 1: Squat {int(squat*0.73)}kg, Bench {int(bench*0.73)}kg, Deadlift {int(deadlift*0.70)}kg
Week 2: Squat {int(squat*0.78)}kg, Bench {int(bench*0.78)}kg, Deadlift {int(deadlift*0.75)}kg
Week 3: Squat {int(squat*0.85)}kg, Bench {int(bench*0.85)}kg, Deadlift {int(deadlift*0.85)}kg
Week 4: Squat {int(squat*0.60)}kg, Bench {int(bench*0.60)}kg, Deadlift {int(deadlift*0.60)}kg

Return ONLY valid JSON (no markdown, no backticks, no extra text before or after). Valid JSON must have:
- "weeks" (list of week objects with "week", "focus", "days")
- "diet" (dict with meal suggestions for {food} diet)
- "tips" (list of 3-5 coaching tips)

Example structure (fill in all values):
{{"weeks": [{{"week": 1, "focus": "Build base", "days": [{{"day_number": 1, "label": "Heavy Squat", "exercises": [{{"name": "Squat", "sets": 4, "reps": 5, "weight": {int(squat*0.73)}, "rpe": 7}}]}}]}}], "diet": {{"meals": [], "calories": {calories}}}, "tips": ["Tip 1", "Tip 2"]}}

Generate the complete {days}-day {goal} program now. Output ONLY the JSON object, nothing else."""

    return prompt