"""
Prompt Builder
Generates personalized, structured training plans via Gemini
"""

from config import *


def get_unified_prompt(stats):
    """
    Build a Gemini prompt requesting a structured program with
    weeks[] -> days[] -> exercises[] and personalized exercises.
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

    # Week focuses for a 4-week cycle
    week_focuses = [
        "Volume and Technique",
        "Intensity Phase",
        "Peaking",
        "Deload",
    ]

    # Build the per-day schema string so Gemini knows exactly how many days
    day_schema_example = ""
    for d in range(1, days + 1):
        day_schema_example += f"""
          {{
            "day_number": {d},
            "label": "Day {d} - Sample Focus",
            "exercises": [
              {{"name": "Sample Exercise A", "sets": 4, "reps": "5", "weight": 80, "rpe": 7, "note": "Sample coaching cue"}},
              {{"name": "Sample Exercise B", "sets": 3, "reps": "8", "weight": 50, "rpe": 6, "note": "Sample coaching cue"}}
            ]
          }}{"," if d < days else ""}"""

    prompt = f"""You are an experienced powerlifting coach — warm, direct, and specific. 🏋️
Use a concise coaching voice throughout (1–2 emojis max in tips/notes). No corporate language.

Generate a fully personalized 4-week training program for the athlete below.

ATHLETE PROFILE:
- Age: {age} | Bodyweight: {bodyweight}kg | Height: {height}cm
- Competition lifts: Squat {squat}kg | Bench {bench}kg | Deadlift {deadlift}kg
- Identified weak point: {weak_point}
- Goal: {goal}
- Training days per week: {days}
- Diet preference: {food}
- Activity level: {activity}

PROGRAMMING REQUIREMENTS:
- 4 weeks total: Week 1 ({week_focuses[0]}), Week 2 ({week_focuses[1]}), Week 3 ({week_focuses[2]}), Week 4 ({week_focuses[3]})
- Each week must have EXACTLY {days} training days
- Each day must have 3-6 exercises tailored to the day's focus
- Exercises must be DIFFERENT across days (e.g. squat day, bench day, deadlift day)
- Include weak-point accessories: since weak point is "{weak_point}", add extra volume for that lift
- For "{goal}" goal: {"use 3-5 rep ranges for strength" if goal in ("Build Strength","Powerbuilding") else "use 8-12 rep ranges for hypertrophy" if goal == "Bulk" else "maintain strength with moderate volume"}
- Scale weights from athlete's maxes: Week1 ~70-75%, Week2 ~75-80%, Week3 ~82-87%, Week4 ~60-65%
- Vary exercise selection across weeks (e.g. flat bench in W1, incline in W2, close-grip in W3, pause bench in W4)
- Add a practical "note" coaching cue for each exercise (specific, actionable, personal to this athlete)

DIET TARGETS (pre-calculated, use exactly these numbers):
- Calories: {calories} kcal | Protein: {protein}g | Carbs: {carbs}g | Fats: {fats}g
- Diet style: {food}
- Generate 4-6 meals appropriate for a {food} athlete training for {goal}

TIPS: Write 5 personalized coaching tips (coach voice, direct, athlete-specific) covering:
- Weak point improvement for {weak_point}
- Key focus for {goal} at {bodyweight}kg
- Recovery for {days} days/week training load
- How to hit {protein}g protein on a {food} diet
- Intensity/progression advice for this 4-week cycle

Return ONLY valid JSON — no markdown, no backticks, no explanation:

{{
  "training": {{
    "summary": "4-week {goal} program for {bodyweight}kg athlete",
    "goal": "{goal}",
    "weeks": [
      {{
        "week": 1,
        "focus": "{week_focuses[0]}",
        "days": [{day_schema_example}
        ]
      }},
      {{
        "week": 2,
        "focus": "{week_focuses[1]}",
        "days": [{day_schema_example}
        ]
      }},
      {{
        "week": 3,
        "focus": "{week_focuses[2]}",
        "days": [{day_schema_example}
        ]
      }},
      {{
        "week": 4,
        "focus": "{week_focuses[3]}",
        "days": [{day_schema_example}
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
      {{"time": "8:00 AM",  "name": "Breakfast",    "food": "Sample {food} breakfast", "protein": 35, "carbs": 65, "fats": 15}},
      {{"time": "11:00 AM", "name": "Mid-Morning",  "food": "Sample snack",             "protein": 25, "carbs": 30, "fats": 10}},
      {{"time": "1:30 PM",  "name": "Lunch",        "food": "Sample {food} lunch",      "protein": 45, "carbs": 70, "fats": 10}},
      {{"time": "4:00 PM",  "name": "Pre-Workout",  "food": "Sample pre-workout meal",  "protein": 15, "carbs": 40, "fats": 8}},
      {{"time": "7:00 PM",  "name": "Post-Workout", "food": "Sample {food} dinner",     "protein": 40, "carbs": 60, "fats": 12}},
      {{"time": "9:30 PM",  "name": "Evening",      "food": "Sample light snack",       "protein": 25, "carbs": 30, "fats": 8}}
    ]
  }},
  "tips": [
    "Actionable tip for improving {weak_point} specific to this athlete",
    "Key insight for {goal} at {bodyweight}kg bodyweight",
    "Recovery tip tailored to {days} training days per week",
    "Practical way to hit {protein}g protein on a {food} diet",
    "Progression cue for this 4-week peaking cycle"
  ]
}}

IMPORTANT RULES:
1. Every week MUST have exactly {days} days in the "days" array.
2. Every day MUST have 4-6 exercises in the "exercises" array.
3. Each exercise MUST have: name, sets (int), reps (string), weight (int kg), rpe (int 1-10), note (string).
4. Do NOT copy the schema placeholders — fill them with real, personalized content.
5. Return ONLY the JSON object. No markdown. No backticks. No explanation."""

    return prompt