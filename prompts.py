"""
Powerlifting AI Coach - Fixed Prompt for Groq
"""

def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, goal, days, food, activity):
    """Generate training program - FIXED JSON"""
    
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

    # FIXED: Escape all quotes, no nested JSON in template
    prompt = f"""You are a powerlifting coach. Design a 4-week {days}-day program.

ATHLETE: Squat {squat}kg, Bench {bench}kg, Deadlift {deadlift}kg, BW {bodyweight}kg, Age {age}, Height {height}cm
WEAK POINT: {weak_point}
GOAL: {goal}
TDEE: {int(tdee)} kcal, TARGET: {calories} kcal, PROTEIN: {protein}g, CARBS: {carbs}g, FATS: {fats}g

WEEKS:
Week 1: 70-75% intensity, high volume, RPE 6-7
Week 2: 75-80% intensity, moderate volume, RPE 7-8
Week 3: 82-87% intensity, low volume, RPE 8-9
Week 4: 60-65% intensity, high volume, RPE 5-6 (deload)

STRATEGY: Vary day order each week. Include recovery days. Make it coaching, not template.

MAIN LIFTS (calculate for each week):
Week 1: Squat {int(squat*0.73)}kg, Bench {int(bench*0.73)}kg, Deadlift {int(deadlift*0.70)}kg
Week 2: Squat {int(squat*0.78)}kg, Bench {int(bench*0.78)}kg, Deadlift {int(deadlift*0.75)}kg
Week 3: Squat {int(squat*0.85)}kg, Bench {int(bench*0.85)}kg, Deadlift {int(deadlift*0.85)}kg
Week 4: Squat {int(squat*0.60)}kg, Bench {int(bench*0.60)}kg, Deadlift {int(deadlift*0.60)}kg

Return ONLY this JSON structure (no markdown, no escaping):

{{
  "summary": "Program for {bodyweight}kg athlete targeting {weak_point}",
  "goal": "{goal}",
  "training_days": {days},
  "weak_point": "{weak_point}",
  "weeks": [
    {{
      "week": 1,
      "focus": "Technique and Volume",
      "day1_ex": [
        {{
          "name": "Back Squat",
          "sets": 5,
          "reps": "5",
          "weight": {int(squat*0.73)},
          "rpe": 6
        }}
      ],
      "day2_ex": [
        {{
          "name": "Bench Press",
          "sets": 5,
          "reps": "5",
          "weight": {int(bench*0.73)},
          "rpe": 6
        }}
      ],
      "day3_ex": [
        {{
          "name": "Deadlifts",
          "sets": 5,
          "reps": "5",
          "weight": {int(deadlift*0.70)},
          "rpe": 6
        }}
      ],
      "day4_ex": [
        {{
          "name": "Speed Bench",
          "sets": 6,
          "reps": "3",
          "weight": {int(bench*0.60)},
          "rpe": 5
        }}
      ]
    }},
    {{
      "week": 2,
      "focus": "Building Phase",
      "day1_ex": [
        {{
          "name": "Deadlifts",
          "sets": 5,
          "reps": "4",
          "weight": {int(deadlift*0.75)},
          "rpe": 7
        }}
      ],
      "day2_ex": [
        {{
          "name": "Back Squat",
          "sets": 5,
          "reps": "4",
          "weight": {int(squat*0.78)},
          "rpe": 7
        }}
      ],
      "day3_ex": [
        {{
          "name": "Bench Press",
          "sets": 5,
          "reps": "4",
          "weight": {int(bench*0.78)},
          "rpe": 7
        }}
      ],
      "day4_ex": [
        {{
          "name": "Speed Squats",
          "sets": 6,
          "reps": "3",
          "weight": {int(squat*0.60)},
          "rpe": 5
        }}
      ]
    }},
    {{
      "week": 3,
      "focus": "Peaking Phase",
      "day1_ex": [
        {{
          "name": "Bench Press",
          "sets": 5,
          "reps": "3",
          "weight": {int(bench*0.85)},
          "rpe": 8
        }}
      ],
      "day2_ex": [
        {{
          "name": "Deadlifts",
          "sets": 5,
          "reps": "3",
          "weight": {int(deadlift*0.85)},
          "rpe": 8
        }}
      ],
      "day3_ex": [
        {{
          "name": "Back Squat",
          "sets": 5,
          "reps": "3",
          "weight": {int(squat*0.85)},
          "rpe": 8
        }}
      ],
      "day4_ex": [
        {{
          "name": "Speed Bench",
          "sets": 5,
          "reps": "2",
          "weight": {int(bench*0.70)},
          "rpe": 6
        }}
      ]
    }},
    {{
      "week": 4,
      "focus": "Deload and Recovery",
      "day1_ex": [
        {{
          "name": "Back Squat",
          "sets": 4,
          "reps": "5",
          "weight": {int(squat*0.60)},
          "rpe": 5
        }}
      ],
      "day2_ex": [
        {{
          "name": "Bench Press",
          "sets": 4,
          "reps": "5",
          "weight": {int(bench*0.60)},
          "rpe": 5
        }}
      ],
      "day3_ex": [
        {{
          "name": "Deadlifts",
          "sets": 3,
          "reps": "5",
          "weight": {int(deadlift*0.60)},
          "rpe": 5
        }}
      ],
      "day4_ex": [
        {{
          "name": "Recovery Walk",
          "sets": 1,
          "reps": "20",
          "weight": 0,
          "rpe": 2
        }}
      ]
    }}
  ],
  "diet": {{
    "calories": {calories},
    "protein": {protein},
    "carbs": {carbs},
    "fats": {fats},
    "maintenance": {int(maintenance)},
    "tdee": {int(tdee)}
  }},
  "tips": [
    "Focus on {weak_point} weak point",
    "Sleep 8+ hours daily",
    "Track every session"
  ]
}}

CRITICAL: Return ONLY the JSON above. No markdown, no backticks, no explanation."""

    return prompt