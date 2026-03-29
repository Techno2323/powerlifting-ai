"""
Simplified Prompt Builder
Returns cleaner JSON responses
"""

from config import *


def get_unified_prompt(stats):
    """
    Simplified prompt for better JSON parsing
    """
    
    squat = stats['squat']
    bench = stats['bench']
    deadlift = stats['deadlift']
    bodyweight = stats['bodyweight']
    height = stats['height']
    age = stats['age']
    goal = stats['goal']
    days = stats['days']
    food = stats['food']
    activity = stats['activity']
    
    # Calculate weak point
    bench_ratio = bench / bodyweight if bodyweight > 0 else 0
    squat_dl_ratio = squat / deadlift if deadlift > 0 else 0
    
    if bench_ratio < BENCH_RATIO_THRESHOLD:
        weak_point = "bench"
    elif squat_dl_ratio < SQUAT_DL_RATIO_THRESHOLD:
        weak_point = "squat"
    else:
        weak_point = "balanced"
    
    # Calculate macros
    maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
    activity_mult = ACTIVITY_MULTIPLIERS.get(activity, 1.55)
    tdee = maintenance * activity_mult
    
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
    
    # Simple, direct prompt
    prompt = f"""You are a powerlifting coach. Generate a program for this athlete:

Age: {age}, Weight: {bodyweight}kg, Height: {height}cm
Squat: {squat}kg, Bench: {bench}kg, Deadlift: {deadlift}kg
Goal: {goal}
Training Days: {days}/week
Diet: {food}
Activity: {activity}
Weak Point: {weak_point}

Generate EXACTLY this JSON format, no markdown, no extra text:

{{
  "training": {{
    "summary": "4-week {goal} program for {bodyweight}kg athlete",
    "goal": "{goal}",
    "weeks": [
      {{
        "week": 1,
        "focus": "Volume and Technique",
        "exercises": [
          {{
            "name": "Back Squat",
            "sets": 5,
            "reps": "5",
            "weight": {int(squat*0.73)},
            "rpe": 6
          }},
          {{
            "name": "Bench Press",
            "sets": 5,
            "reps": "5",
            "weight": {int(bench*0.73)},
            "rpe": 6
          }},
          {{
            "name": "Deadlift",
            "sets": 3,
            "reps": "5",
            "weight": {int(deadlift*0.70)},
            "rpe": 6
          }},
          {{
            "name": "Leg Press",
            "sets": 3,
            "reps": "8",
            "weight": {int(squat*0.90)},
            "rpe": 7
          }},
          {{
            "name": "Dumbbell Press",
            "sets": 3,
            "reps": "8",
            "weight": 30,
            "rpe": 7
          }}
        ]
      }},
      {{
        "week": 2,
        "focus": "Building Phase",
        "exercises": [
          {{
            "name": "Deadlift",
            "sets": 5,
            "reps": "4",
            "weight": {int(deadlift*0.75)},
            "rpe": 7
          }},
          {{
            "name": "Back Squat",
            "sets": 5,
            "reps": "4",
            "weight": {int(squat*0.78)},
            "rpe": 7
          }},
          {{
            "name": "Bench Press",
            "sets": 5,
            "reps": "4",
            "weight": {int(bench*0.78)},
            "rpe": 7
          }},
          {{
            "name": "Leg Press",
            "sets": 3,
            "reps": "8",
            "weight": {int(squat*0.95)},
            "rpe": 7
          }},
          {{
            "name": "Cable Fly",
            "sets": 3,
            "reps": "10",
            "weight": 20,
            "rpe": 7
          }}
        ]
      }},
      {{
        "week": 3,
        "focus": "Peaking",
        "exercises": [
          {{
            "name": "Back Squat",
            "sets": 5,
            "reps": "3",
            "weight": {int(squat*0.85)},
            "rpe": 8
          }},
          {{
            "name": "Bench Press",
            "sets": 5,
            "reps": "3",
            "weight": {int(bench*0.85)},
            "rpe": 8
          }},
          {{
            "name": "Deadlift",
            "sets": 5,
            "reps": "3",
            "weight": {int(deadlift*0.85)},
            "rpe": 8
          }},
          {{
            "name": "Leg Curl",
            "sets": 3,
            "reps": "10",
            "weight": 80,
            "rpe": 7
          }},
          {{
            "name": "Incline Bench",
            "sets": 3,
            "reps": "6",
            "weight": {int(bench*0.70)},
            "rpe": 7
          }}
        ]
      }},
      {{
        "week": 4,
        "focus": "Deload",
        "exercises": [
          {{
            "name": "Back Squat",
            "sets": 3,
            "reps": "5",
            "weight": {int(squat*0.60)},
            "rpe": 5
          }},
          {{
            "name": "Bench Press",
            "sets": 3,
            "reps": "5",
            "weight": {int(bench*0.60)},
            "rpe": 5
          }},
          {{
            "name": "Deadlift",
            "sets": 3,
            "reps": "3",
            "weight": {int(deadlift*0.60)},
            "rpe": 5
          }},
          {{
            "name": "Walk",
            "sets": 1,
            "reps": "20",
            "weight": 0,
            "rpe": 2
          }},
          {{
            "name": "Stretch",
            "sets": 1,
            "reps": "15",
            "weight": 0,
            "rpe": 1
          }}
        ]
      }}
    ]
  }},
  "diet": {{
    "calories": {calories},
    "protein": {protein},
    "carbs": {carbs},
    "fats": {fats},
    "maintenance": {int(maintenance)},
    "tdee": {int(tdee)},
    "meals": [
      {{
        "time": "8:00 AM",
        "name": "Breakfast",
        "food": "3 eggs + 1 cup oats + 1 banana",
        "protein": 35,
        "carbs": 65,
        "fats": 15
      }},
      {{
        "time": "11:00 AM",
        "name": "Mid-Morning",
        "food": "Protein shake + almonds",
        "protein": 30,
        "carbs": 35,
        "fats": 12
      }},
      {{
        "time": "1:30 PM",
        "name": "Lunch",
        "food": "Chicken rice with veggies",
        "protein": 45,
        "carbs": 70,
        "fats": 10
      }},
      {{
        "time": "4:00 PM",
        "name": "Pre-Workout",
        "food": "Banana + peanut butter",
        "protein": 12,
        "carbs": 45,
        "fats": 8
      }},
      {{
        "time": "7:00 PM",
        "name": "Post-Workout",
        "food": "Eggs + rice + broccoli",
        "protein": 40,
        "carbs": 60,
        "fats": 12
      }},
      {{
        "time": "9:30 PM",
        "name": "Evening",
        "food": "Greek yogurt + granola",
        "protein": 25,
        "carbs": 35,
        "fats": 8
      }}
    ]
  }},
  "tips": [
    "Your {weak_point} is weaker than other lifts. Focus on paused reps and accessories for this lift.",
    "At {age} years old, your recovery is excellent. Leverage high volume training with proper sleep.",
    "For {goal}, balance heavy compounds (3-5 reps) with hypertrophy work (8-12 reps).",
    "Your {food} diet works well. Get protein from varied sources throughout the day.",
    "With {days} training days, you have enough volume. Track progress weekly and adjust intensity."
  ]
}}

CRITICAL: Return ONLY the JSON above. No markdown. No backticks. No explanation."""

    return prompt