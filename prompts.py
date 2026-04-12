# prompt.py - Nippard-Inspired Elite Prompt Engine

def classify_experience(years_training: float) -> dict:
    if years_training < 1:
        return {
            "tier": "Beginner",
            "exercise_complexity": "LOW",
            "directives": (
                "- Use ONLY fundamental barbell + machine movements. No complex variations.\n"
                "- Prioritize motor pattern learning: goblet squat, leg press, lat pulldown, DB bench.\n"
                "- NEVER program paused variations, tempo work, or accommodating resistance.\n"
                "- Keep RPE 6-7. Athlete is still learning to gauge effort accurately.\n"
                "- Linear progression: add 2.5kg per week on main lifts when all reps completed.\n"
                "- 1 top set only on primary lifts — no back-off sets yet, too fatiguing."
            ),
            "periodization": "Linear Progression — same exercises weekly, add weight each session",
            "top_set_rpe": "7",
            "backoff_rpe": "N/A",
            "volume_modifier": 0.7,
            "intensity_bracket": "65-75%",
            "use_backoff_sets": False,
        }
    elif years_training < 3:
        return {
            "tier": "Intermediate",
            "exercise_complexity": "MODERATE",
            "directives": (
                "- Use TOP SET + BACK-OFF SET structure on primary lifts.\n"
                "- Top set: 1 heavy set at RPE 8-8.5 using intensity bracket.\n"
                "- Back-off sets: 2-3 sets at fixed %1RM (7.5-10% below top set), RPE N/A.\n"
                "- Introduce barbell variations: paused squats, close-grip bench, deficit deadlifts.\n"
                "- RPE range 7-9. Athlete can self-regulate intensity effectively.\n"
                "- Block periodization: accumulation → strength → peaking → deload across 4 weeks.\n"
                "- Include 1 weak-point variation per main lift day as secondary exercise."
            ),
            "periodization": "Block Periodization — accumulation W1→ intensification W2→ peaking W3→ deload W4",
            "top_set_rpe": "8-8.5",
            "backoff_rpe": "N/A (fixed %)",
            "volume_modifier": 0.85,
            "intensity_bracket": "75-87.5%",
            "use_backoff_sets": True,
        }
    elif years_training < 5:
        return {
            "tier": "Advanced",
            "exercise_complexity": "HIGH",
            "directives": (
                "- Use TOP SET + BACK-OFF SET structure. Top set RPE 8.5-9.\n"
                "- Program complex variations: pin squats, board press, block pulls, pause variations.\n"
                "- High frequency: squat and bench 2x/week each, deadlift 1-2x/week.\n"
                "- Use intensity brackets on top sets for daily autoregulation.\n"
                "- Back-off sets at fixed %1RM to accumulate specific volume.\n"
                "- Planned overreach in Week 3 with deload in Week 4 for supercompensation.\n"
                "- Circuit-style accessories (A1/A2) to manage time and density."
            ),
            "periodization": "Conjugate-influenced Block — daily undulating + weekly undulating periodization",
            "top_set_rpe": "8.5-9",
            "backoff_rpe": "N/A (fixed %)",
            "volume_modifier": 1.0,
            "intensity_bracket": "80-92.5%",
            "use_backoff_sets": True,
        }
    else:
        return {
            "tier": "Elite",
            "exercise_complexity": "VERY HIGH",
            "directives": (
                "- Competition-specific meet-prep periodization with full autoregulation.\n"
                "- Top sets: RPE 8.5-9.5 with intensity brackets for daily readiness adjustment.\n"
                "- Back-off sets: 2-3 sets at fixed %1RM immediately after top set.\n"
                "- Program speed/dynamic effort work at 50-60% for bar speed development.\n"
                "- Advanced techniques: cluster sets, rest-pause, isometric holds at sticking points.\n"
                "- Circuit accessories (A1/A2/B1/B2) to maximize density.\n"
                "- Include competition commands: pause bench, squat to depth commands.\n"
                "- Strategic semi-deloads mid-block (like Nippard Week 6) before peak."
            ),
            "periodization": "Autoregulated Conjugate — reactive daily adjustments based on readiness",
            "top_set_rpe": "8.5-9.5",
            "backoff_rpe": "N/A (fixed %)",
            "volume_modifier": 1.0,
            "intensity_bracket": "82.5-95%",
            "use_backoff_sets": True,
        }


GOAL_TRAINING_PARAMS = {
    "Cut": {
        "rep_range_primary": "3-6 (keep strength)",
        "rep_range_secondary": "10-15 (metabolic)",
        "intensity_primary": "80-87.5% 1RM",
        "volume_level": "Moderate — preserve muscle, manage fatigue under deficit",
        "rest_primary": "2-3 min",
        "rest_secondary": "45-75s",
        "exercise_count_per_day": "5-6",
        "rpe_ceiling": 8,
        "set_range_primary": "3-4",
        "set_range_secondary": "2-3",
        "special_instructions": (
            "- MUSCLE PRESERVATION is the priority, not building.\n"
            "- Keep main lift intensity high (80%+) but reduce total volume 15-20%.\n"
            "- Add 1 metabolic finisher (superset/circuit) at session end to increase calorie burn.\n"
            "- Shorten rest on accessories to 45-75s to maintain elevated heart rate.\n"
            "- Reduce accessory volume first if recovery is compromised.\n"
            "- NO heavy singles or triples in Week 3 — injury risk elevated in deficit.\n"
            "- Protein intake critical: remind athlete to eat 2.2g/kg bodyweight minimum."
        ),
    },
    "Bulk": {
        "rep_range_primary": "3-6 (strength base)",
        "rep_range_secondary": "8-12 (hypertrophy)",
        "intensity_primary": "75-87.5% 1RM",
        "volume_level": "High — maximize hypertrophy with caloric surplus",
        "rest_primary": "3-4 min",
        "rest_secondary": "60-90s",
        "exercise_count_per_day": "5-7",
        "rpe_ceiling": 9,
        "set_range_primary": "3-5",
        "set_range_secondary": "3-4",
        "special_instructions": (
            "- Progressive overload through VOLUME first, then load.\n"
            "- Include back-off sets on primary lifts: 2 sets at 7.5% below top set.\n"
            "- Target weak muscle groups with extra accessory sets.\n"
            "- Mix compound and isolation: 60/40 split per session.\n"
            "- Higher rep ranges on accessories: 10-15 for hypertrophy stimulus.\n"
            "- Can push RPE to 9 on accessories; keep compounds at 7.5-8.5.\n"
            "- Superset isolation movements (arms/shoulders) to save time and add density."
        ),
    },
    "Build Strength": {
        "rep_range_primary": "1-5 (strength focus)",
        "rep_range_secondary": "6-10 (strength-hypertrophy)",
        "intensity_primary": "80-95% 1RM",
        "volume_level": "Moderate-Low — CNS-intensive, quality reps over quantity",
        "rest_primary": "3-5 min",
        "rest_secondary": "2-3 min",
        "exercise_count_per_day": "4-6",
        "rpe_ceiling": 9.5,
        "set_range_primary": "3-5",
        "set_range_secondary": "2-3",
        "special_instructions": (
            "- Main lifts are KING — 60%+ of session time on SBD and close variations.\n"
            "- Use TOP SET + BACK-OFF SET structure: 1 heavy top set then 2 back-off sets at fixed %.\n"
            "- Week 1: Volume accumulation 75-80% top set. Week 2: Intensification 80-87.5%.\n"
            "- Week 3: Peaking 87.5-92.5% with low volume. Week 4: Deload 60-70%.\n"
            "- Rest MUST be 3-5 min between primary working sets — non-negotiable for CNS recovery.\n"
            "- Accessories are for injury prevention and weak points only (2-3 per session).\n"
            "- Include paused variations as technique work: paused squat, paused bench."
        ),
    },
    "Powerbuilding": {
        "rep_range_primary": "3-6 (strength)",
        "rep_range_secondary": "8-12 (hypertrophy)",
        "intensity_primary": "80-90% 1RM",
        "volume_level": "High — combining strength + hypertrophy demands simultaneously",
        "rest_primary": "3-4 min",
        "rest_secondary": "60-90s",
        "exercise_count_per_day": "5-7",
        "rpe_ceiling": 9,
        "set_range_primary": "3-5",
        "set_range_secondary": "3-4",
        "special_instructions": (
            "- HYBRID approach: heavy compound work (3-6 reps) + hypertrophy accessory work (8-12 reps).\n"
            "- Structure: 1 TOP SET heavy → 2 BACK-OFF SETS at 7.5% below → transition to hypertrophy accessories.\n"
            "- Primary movements: competition SBD + close variations at 80-90% 1RM.\n"
            "- Secondary: barbell variations (paused, close grip, deficit) at 75-82.5%.\n"
            "- Tertiary: DB work, cables, machines at 8-12 reps for hypertrophy and pump.\n"
            "- Use CIRCUIT supersets (A1/A2) for isolation work (arms, shoulders, calves) to save time.\n"
            "- Include at least 1 pump finisher per session: high-rep curls, lateral raises, face pulls.\n"
            "- Balance push:pull ratio 1:1 across the week to prevent imbalances.\n"
            "- This athlete wants to LOOK strong AND BE strong — program accordingly."
        ),
    },
}


def detect_weak_points(squat, bench, deadlift, bodyweight, gender):
    weak_points = []
    bw = max(bodyweight, 1)
    sq_ratio = squat / bw
    bn_ratio = bench / bw
    dl_ratio = deadlift / bw

    if gender.lower() in ["male", "m"]:
        if bn_ratio < 1.25:
            weak_points.append({
                "lift": "bench",
                "issue": "underdeveloped upper body pressing",
                "fix": "add close-grip bench, dips, and tricep volume"
            })
        if sq_ratio < 1.5:
            weak_points.append({
                "lift": "squat",
                "issue": "below intermediate squat standards",
                "fix": "add pause squats, good mornings, and quad isolation"
            })
        if dl_ratio < 1.75:
            weak_points.append({
                "lift": "deadlift",
                "issue": "below intermediate deadlift standards",
                "fix": "add rack pulls, deficit deadlifts, and lat work"
            })
        if squat > 0 and deadlift > 0 and (deadlift / squat) < 1.1:
            weak_points.append({
                "lift": "posterior chain",
                "issue": "deadlift:squat ratio too low — posterior chain underdeveloped",
                "fix": "add RDLs, good mornings, nordic ham curls every session"
            })
        if squat > 0 and deadlift > 0 and (deadlift / squat) > 1.6:
            weak_points.append({
                "lift": "quad strength",
                "issue": "squat:deadlift ratio too low — quads underdeveloped",
                "fix": "add leg press, pause squats, and front squats"
            })
    else:
        if bn_ratio < 0.75:
            weak_points.append({
                "lift": "bench",
                "issue": "underdeveloped upper body pressing",
                "fix": "add dumbbell press, dips, and tricep volume"
            })
        if sq_ratio < 1.25:
            weak_points.append({
                "lift": "squat",
                "issue": "below intermediate squat standards",
                "fix": "add pause squats, Bulgarian split squats, and quad isolation"
            })
        if dl_ratio < 1.5:
            weak_points.append({
                "lift": "deadlift",
                "issue": "below intermediate deadlift standards",
                "fix": "add RDLs, hip thrusts, and rack pulls"
            })

    if not weak_points:
        weak_points.append({
            "lift": "balanced",
            "issue": "all lifts proportional",
            "fix": "focus on overall progressive overload — no specific weak points identified"
        })

    return weak_points


def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, gender,
                        goal, days, food, activity, years_training=1.0, target_week=1):

    exp = classify_experience(years_training)
    goal_params = GOAL_TRAINING_PARAMS.get(goal, GOAL_TRAINING_PARAMS["Build Strength"])
    weak_points = detect_weak_points(squat, bench, deadlift, bodyweight, gender)

    # Weak point summary for prompt
    weak_str = "; ".join([f"{w['lift']} ({w['issue']}) → fix: {w['fix']}" for w in weak_points])

    # Calorie calculation (Mifflin-St Jeor)
    if gender.lower() in ["male", "m"]:
        bmr = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * bodyweight) + (6.25 * height) - (5 * age) - 161

    activity_multipliers = {
        "Sedentary": 1.2, "Light": 1.375,
        "Moderate": 1.55, "Very Active": 1.725
    }
    tdee = bmr * activity_multipliers.get(activity, 1.55)
    calorie_adjustments = {"Build Strength": 200, "Bulk": 500, "Cut": -500, "Powerbuilding": 300}
    target_calories = int(tdee + calorie_adjustments.get(goal, 200))
    target_protein = int(bodyweight * 2.2)
    target_carbs = int(bodyweight * (5.0 if goal == "Bulk" else 4.5 if goal == "Build Strength" else 3.5))
    target_fats = int(bodyweight * (1.0 if goal != "Cut" else 0.8))

    # Strength level descriptor
    total = squat + bench + deadlift
    rel = total / max(bodyweight, 1)
    if rel >= 7: strength_desc = "elite-level totals"
    elif rel >= 5.5: strength_desc = "advanced, approaching competition level"
    elif rel >= 4: strength_desc = "solid intermediate with good foundation"
    elif rel >= 2.5: strength_desc = "novice-intermediate, building base strength"
    else: strength_desc = "beginner — prioritize technique over load"

    # Week-specific intensity percentages based on Nippard's structure
    week_data = {
        1: {
            "name": "Accumulation",
            "desc": "Build work capacity. Top sets 75-80% 1RM. Back-off sets 70-75%. Higher reps (5-8). Establish movement patterns.",
            "top_set_pct": {"squat": round(squat * 0.775 / 2.5) * 2.5,
                           "bench": round(bench * 0.775 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.775 / 2.5) * 2.5},
            "backoff_pct": {"squat": round(squat * 0.70 / 2.5) * 2.5,
                           "bench": round(bench * 0.70 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.70 / 2.5) * 2.5},
            "top_rpe": "7.5-8",
            "volume": "higher (3-4 back-off sets)",
        },
        2: {
            "name": "Intensification",
            "desc": "Increase load, reduce volume slightly. Top sets 82.5-87.5% 1RM. Fewer reps (3-5). Push harder on top sets.",
            "top_set_pct": {"squat": round(squat * 0.85 / 2.5) * 2.5,
                           "bench": round(bench * 0.85 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.85 / 2.5) * 2.5},
            "backoff_pct": {"squat": round(squat * 0.775 / 2.5) * 2.5,
                           "bench": round(bench * 0.775 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.775 / 2.5) * 2.5},
            "top_rpe": "8-8.5",
            "volume": "moderate (2-3 back-off sets)",
        },
        3: {
            "name": "Peaking",
            "desc": "Highest intensity. Top sets 87.5-92.5% 1RM. Low volume. Heavy doubles/triples. This week should feel HARD.",
            "top_set_pct": {"squat": round(squat * 0.90 / 2.5) * 2.5,
                           "bench": round(bench * 0.90 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.90 / 2.5) * 2.5},
            "backoff_pct": {"squat": round(squat * 0.825 / 2.5) * 2.5,
                           "bench": round(bench * 0.825 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.825 / 2.5) * 2.5},
            "top_rpe": "8.5-9",
            "volume": "low (2 back-off sets maximum)",
        },
        4: {
            "name": "Deload",
            "desc": "Reduce ALL loads to 60-65% 1RM. Cut volume by 40-50%. Active recovery. The body rebuilds and supercompensates here.",
            "top_set_pct": {"squat": round(squat * 0.625 / 2.5) * 2.5,
                           "bench": round(bench * 0.625 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.625 / 2.5) * 2.5},
            "backoff_pct": {"squat": round(squat * 0.60 / 2.5) * 2.5,
                           "bench": round(bench * 0.60 / 2.5) * 2.5,
                           "deadlift": round(deadlift * 0.60 / 2.5) * 2.5},
            "top_rpe": "5-6",
            "volume": "minimal (1-2 sets, technique focus only)",
        },
    }

    w = week_data.get(target_week, week_data[1])

    # Build JSON schema — only for week 1 include diet/summary/tips
    if target_week == 1:
        schema = f"""Return ONLY valid JSON. No markdown, no backticks, no extra text.

Root object must have:
- "summary": 2 sentences personalised to THIS athlete (mention their actual squat/bench/deadlift numbers)
- "goal": string
- "training_days": integer  
- "weak_points": string (from analysis above)
- "experience_level": string
- "week": 1
- "focus": string (week 1 phase name and key objective)
- "calories": {target_calories}
- "protein": {target_protein}
- "carbs": {target_carbs}
- "fats": {target_fats}
- "meals": array of meal objects (6 meals minimum, Indian foods only for {food} diet)
  Each meal: "time", "name", "food" (specific with quantities), "protein", "carbs", "fats"
- "tips": array of exactly 4 strings (personalised coaching tips referencing THIS athlete's stats)
- "day1_ex" through "day{days}_ex": arrays of exercise objects

Each exercise object:
- "name": concise name (e.g. "Squat" not "High-Bar Back Squat")
- "sets": integer
- "reps": string (e.g. "5", "3-5", "8-10", "AMRAP")
- "weight": integer in kg (calculated from their actual 1RMs)
- "rpe": number (can be decimal like 7.5, or "N/A" for back-off sets at fixed %)
- "rest": string (e.g. "3-4 min", "60-90s", "30s")
- "notes": 1 specific coaching cue (movement-specific, not generic)
- "type": string ("primary_top", "primary_backoff", "secondary", "tertiary", or "circuit_A1/A2")"""
    else:
        schema = f"""Return ONLY valid JSON. No markdown, no backticks, no extra text.

Root object must have:
- "week": {target_week}
- "focus": string (week {target_week} phase and objective)
- "day1_ex" through "day{days}_ex": arrays of exercise objects

Each exercise object:
- "name": concise name
- "sets": integer
- "reps": string
- "weight": integer in kg
- "rpe": number or "N/A"
- "rest": string
- "notes": 1 specific coaching cue
- "type": string ("primary_top", "primary_backoff", "secondary", "tertiary", or "circuit_A1/A2")"""

    prompt = f"""You are an ELITE strength coach trained in Jeff Nippard's evidence-based powerbuilding methodology. You think like a real coach — not a template generator.

Your task: Design Week {target_week} ("{w['name']}") of a 4-week {days}-day training block for a specific athlete.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATHLETE PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gender: {gender} | Age: {age} | Bodyweight: {bodyweight}kg | Height: {height}cm
Training Experience: {years_training} years → {exp["tier"]} level
Current 1RMs: Squat {squat}kg | Bench {bench}kg | Deadlift {deadlift}kg
SBD Total: {total}kg ({strength_desc})
Identified Weak Points: {weak_str}
Primary Goal: {goal}
Training Days: {days}/week
Activity Level: {activity}
Diet Preference: {food}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEEK {target_week} — {w['name'].upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase description: {w['desc']}
Top set RPE target: {w['top_rpe']}
Volume: {w['volume']}

PRE-CALCULATED WORKING WEIGHTS (use these exactly, rounded to 2.5kg):
- Squat top set: {w['top_set_pct']['squat']}kg | Back-off sets: {w['backoff_pct']['squat']}kg
- Bench top set: {w['top_set_pct']['bench']}kg | Back-off sets: {w['backoff_pct']['bench']}kg  
- Deadlift top set: {w['top_set_pct']['deadlift']}kg | Back-off sets: {w['backoff_pct']['deadlift']}kg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXPERIENCE DIRECTIVES ({exp["tier"]})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{exp["directives"]}
Periodization: {exp["periodization"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOAL PARAMETERS ({goal})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary rep range: {goal_params["rep_range_primary"]}
Secondary rep range: {goal_params["rep_range_secondary"]}
Primary intensity: {goal_params["intensity_primary"]}
Volume level: {goal_params["volume_level"]}
Rest (primary): {goal_params["rest_primary"]} | Rest (secondary): {goal_params["rest_secondary"]}
Exercises per session: {goal_params["exercise_count_per_day"]}
{goal_params["special_instructions"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIPPARD-STYLE PROGRAMMING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. TOP SET + BACK-OFF SET STRUCTURE on primary lifts:
   - 1 top set at the pre-calculated weight above (RPE {w['top_rpe']})
   - 2-3 back-off sets at the back-off weight (RPE "N/A" — fixed %)
   - This is how Nippard programs — heavy single top set then volume work

2. EXERCISE HIERARCHY per session:
   - Primary (type: "primary_top" + "primary_backoff"): 1 main competition lift
   - Secondary (type: "secondary"): 1-2 barbell variations targeting weak points
   - Tertiary (type: "tertiary"): 2-3 isolation/machine movements
   - Circuit (type: "circuit_A1/A2"): pair isolation exercises to save time

3. SESSION STRUCTURE varies by day type:
   - Heavy SBD day: 1 primary + 2-3 secondary + 1-2 tertiary = 4-5 exercises
   - Hypertrophy day: 1 primary + 2 secondary + 3-4 tertiary/circuit = 6-7 exercises
   - NOT every day needs all 3 lifts — intelligent programming distributes stimulus

4. INTENSITY VARIES across days within the week:
   - Day with heavy squat at 90% → that day's bench is lighter (technique/volume)
   - Never program 3 heavy compound movements on the same day

5. EXERCISE SELECTION addresses weak points:
   - Weak: {weak_str}
   - Include at least 1 exercise per session that targets the identified weak point

6. COACHING CUES must be movement-specific:
   - Good: "Drive knees out, chest up, explode out of the hole"
   - Bad: "Focus on form" (too generic — this is a failing answer)

7. FACE PULLS or BAND PULL-APARTS must appear at least once per week for shoulder health

8. DELOAD WEEK (Week 4) rules:
   - No RPE above 6
   - Maximum 2-3 working sets per exercise
   - Focus on technique refinement and movement quality

{schema}
"""
    return prompt