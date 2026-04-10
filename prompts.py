"""
Powerlifting AI Coach - Elite Prompt Engine
Generates deeply personalized, experience-aware, goal-driven training programs.
"""
import json


# ── Experience Level Classification ──────────────────────────────────────────

def classify_experience(years_training: float) -> dict:
    """Return experience tier + coaching directives based on training age."""
    if years_training < 1:
        return {
            "tier": "Beginner",
            "exercise_complexity": "LOW",
            "directives": (
                "- Use ONLY fundamental compound barbell movements + machines for stability.\n"
                "- Prioritize learning motor patterns: goblet squats, leg press, lat pulldown, "
                "DB bench, cable rows over advanced barbell variations.\n"
                "- NEVER program Olympic lifts, banded work, chains, or paused variations.\n"
                "- Keep RPE between 6-8; the athlete is still learning to gauge effort.\n"
                "- Include 1-2 machine-based isolation exercises per session for safe volume.\n"
                "- Prefer linear progression: add 2.5kg per week on main lifts."
            ),
            "periodization": "Linear Progression (simple A/B or full-body rotation)",
            "rpe_range": "6-8",
            "volume_modifier": 0.7,
        }
    elif years_training < 3:
        return {
            "tier": "Intermediate",
            "exercise_complexity": "MODERATE",
            "directives": (
                "- Introduce barbell variations: paused squats, close-grip bench, deficit deadlifts.\n"
                "- Add unilateral work: Bulgarian split squats, single-arm DB rows, lunges.\n"
                "- RPE should range 7-9; the athlete can self-regulate intensity.\n"
                "- Can handle moderate complexity: tempo work, controlled eccentrics.\n"
                "- Use daily undulating periodization (DUP) or block periodization.\n"
                "- Include 1 technique/weak-point variation per main lift day."
            ),
            "periodization": "Block Periodization (hypertrophy → strength → peaking → deload)",
            "rpe_range": "7-9",
            "volume_modifier": 0.85,
        }
    elif years_training < 5:
        return {
            "tier": "Advanced",
            "exercise_complexity": "HIGH",
            "directives": (
                "- Program complex multi-joint movements: pin squats, board press, block pulls.\n"
                "- Include banded/chain accommodating resistance on main lifts.\n"
                "- RPE should range 7.5-9.5 with strategic overreaching weeks.\n"
                "- Use conjugate or Westside-inspired rotations for variation.\n"
                "- Can handle high-frequency training (SBD 2x/week each).\n"
                "- Include sport-specific accessory work targeting competition carryover.\n"
                "- Program planned overreach in Week 3 with supercompensation in Week 4."
            ),
            "periodization": "Conjugate / Advanced Block (accumulation → transmutation → realization)",
            "rpe_range": "7.5-9.5",
            "volume_modifier": 1.0,
        }
    else:
        return {
            "tier": "Elite",
            "exercise_complexity": "VERY HIGH",
            "directives": (
                "- Full competition-specific programming with meet-prep periodization.\n"
                "- Program accommodating resistance (bands/chains) on 40%+ of working sets.\n"
                "- Include speed/dynamic effort work at 50-60% with bands.\n"
                "- RPE range 8-10 with autoregulation built into every session.\n"
                "- Advanced techniques: cluster sets, rest-pause, isometric holds at sticking points.\n"
                "- Minimal form regression expected — can handle max-effort singles.\n"
                "- Weekly undulation with daily autoregulation based on readiness.\n"
                "- Extensive warm-up protocols and competition-specific commands (pause, rack)."
            ),
            "periodization": "Autoregulated Conjugate / Reactive (readiness-driven daily adjustments)",
            "rpe_range": "8-10",
            "volume_modifier": 1.0,
        }


# ── Goal-Specific Training Parameters ───────────────────────────────────────

GOAL_TRAINING_PARAMS = {
    "Cut": {
        "rep_range": "8-12",
        "intensity_range": "70-80% 1RM",
        "volume_level": "Moderate (preserve muscle, manage fatigue under caloric deficit)",
        "frequency": "4-5 days/week",
        "rest_periods": "45-75 seconds between sets",
        "exercise_count_per_day": "5-6",
        "rpe_ceiling": 8,
        "set_range": "3-4",
        "special_instructions": (
            "- Priority is MUSCLE PRESERVATION, not building.\n"
            "- Keep main lift intensity high (80%+) but reduce total volume by ~20%.\n"
            "- Add 1-2 metabolic finishers (supersets, circuits) at end of sessions.\n"
            "- Shorter rest periods to maintain elevated heart rate.\n"
            "- Reduce accessory volume first if recovery is compromised.\n"
            "- Do NOT program heavy singles or triples — injury risk is elevated in a deficit."
        ),
    },
    "Bulk": {
        "rep_range": "6-12",
        "intensity_range": "75-85% 1RM",
        "volume_level": "High (maximize hypertrophy with caloric surplus)",
        "frequency": "4-5 days/week",
        "rest_periods": "60-90 seconds between sets",
        "exercise_count_per_day": "5-7",
        "rpe_ceiling": 9,
        "set_range": "3-5",
        "special_instructions": (
            "- Emphasize progressive overload through VOLUME first, then load.\n"
            "- Include drop sets or back-off sets on main lifts (1-2x per week).\n"
            "- Target weak muscle groups with 2-3 extra accessory sets per week.\n"
            "- Mix compound and isolation work: 60/40 split.\n"
            "- Higher carb timing around training for performance.\n"
            "- Can push RPE to 9 on accessories; keep compounds at 7-8.5."
        ),
    },
    "Build Strength": {
        "rep_range": "1-5",
        "intensity_range": "85-95% 1RM",
        "volume_level": "Moderate-Low (CNS-intensive, quality reps)",
        "frequency": "3-4 days/week",
        "rest_periods": "2-4 minutes between working sets",
        "exercise_count_per_day": "3-5",
        "rpe_ceiling": 9.5,
        "set_range": "3-6",
        "special_instructions": (
            "- Main lifts are KING — spend 60%+ of session time on SBD and close variations.\n"
            "- Heavy singles/doubles at RPE 8-9 in Weeks 2-3.\n"
            "- Week 1: Volume accumulation at 80-85%. Week 2: Intensification at 85-90%.\n"
            "- Week 3: Peaking at 90-95% with reduced volume. Week 4: Deload at 60-70%.\n"
            "- Rest periods MUST be 2-4 minutes for main lifts — this is non-negotiable.\n"
            "- Accessories are for injury prevention and weak points only (2-3 per session).\n"
            "- Competition-style commands: include paused bench, commands at lockout."
        ),
    },
    "Powerbuilding": {
        "rep_range": "3-8 (primary), 8-12 (accessories)",
        "intensity_range": "80-92% 1RM (primary), 65-75% (accessories)",
        "volume_level": "High (combining strength + hypertrophy demands)",
        "frequency": "4-5 days/week",
        "rest_periods": "2-3 min for compounds, 60-90s for accessories",
        "exercise_count_per_day": "5-7",
        "rpe_ceiling": 9,
        "set_range": "3-5",
        "special_instructions": (
            "- HYBRID approach: heavy compound work (3-5 reps) followed by hypertrophy accessory work (8-12 reps).\n"
            "- Each session starts with 1-2 heavy barbell movements then transitions to bodybuilding-style volume.\n"
            "- Primary movements: competition SBD + close variations at 80-92% 1RM.\n"
            "- Secondary movements: DB work, cables, machines at 65-75% for 8-12 reps.\n"
            "- Include at least one 'pump' finisher per session (e.g. high-rep curls, lateral raises, face pulls).\n"
            "- Balance pushing and pulling volume 1:1 to prevent structural imbalances.\n"
            "- This athlete wants to LOOK strong AND BE strong — program accordingly."
        ),
    },
}


# ── Weak Point Detection ────────────────────────────────────────────────────

def detect_weak_points(squat, bench, deadlift, bodyweight, gender):
    """Analyze lift ratios to identify weak points with specific recommendations."""
    weak_points = []
    
    bw = max(bodyweight, 1)
    sq_ratio = squat / bw
    bn_ratio = bench / bw
    dl_ratio = deadlift / bw
    
    # Gender-specific strength standards (intermediate level benchmarks)
    if gender.lower() == "male":
        if bn_ratio < 1.25:
            weak_points.append("bench (underdeveloped upper body pressing strength)")
        if sq_ratio < 1.5:
            weak_points.append("squat (below intermediate squat standards)")
        if dl_ratio < 1.75:
            weak_points.append("deadlift (below intermediate deadlift standards)")
        if squat > 0 and deadlift > 0 and (deadlift / squat) < 1.1:
            weak_points.append("posterior chain (deadlift:squat ratio is too low)")
        if squat > 0 and deadlift > 0 and (deadlift / squat) > 1.5:
            weak_points.append("quad dominance deficit (squat:deadlift ratio is too low)")
    else:
        if bn_ratio < 0.75:
            weak_points.append("bench (underdeveloped upper body pressing strength)")
        if sq_ratio < 1.25:
            weak_points.append("squat (below intermediate squat standards)")
        if dl_ratio < 1.5:
            weak_points.append("deadlift (below intermediate deadlift standards)")
    
    if not weak_points:
        weak_points.append("balanced (all lifts proportional — focus on overall progression)")
    
    return weak_points


# ── Main Prompt Generator ───────────────────────────────────────────────────

def get_coaching_prompt(squat, bench, deadlift, bodyweight, height, age, gender,
                        goal, days, food, activity, years_training=0, target_week=1):
    """Generate an elite, deeply personalized training prompt for Gemini."""

    # ── Classify experience ──
    exp = classify_experience(years_training)

    # ── Get goal-specific training parameters ──
    goal_params = GOAL_TRAINING_PARAMS.get(goal, GOAL_TRAINING_PARAMS["Build Strength"])

    # ── Detect weak points ──
    weak_points = detect_weak_points(squat, bench, deadlift, bodyweight, gender)
    weak_points_str = "; ".join(weak_points)

    # ── Calculate calorie targets (for diet object) ──
    if gender.lower() == "male":
        maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) + 5
    else:
        maintenance = (10 * bodyweight) + (6.25 * height) - (5 * age) - 161

    activity_multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Very Active": 1.725}
    tdee = maintenance * activity_multipliers.get(activity, 1.55)

    calorie_adjustments = {
        "Build Strength": 300,
        "Bulk": 500,
        "Cut": -500,
        "Powerbuilding": 400,
    }
    calories = int(tdee + calorie_adjustments.get(goal, 300))
    protein = int(bodyweight * 2.2)
    carbs = int(bodyweight * 5.5)
    fats = int(bodyweight * 1.1)

    # ── Wilks-approximation strength level description ──
    total = squat + bench + deadlift
    if total > 0:
        relative_total = total / max(bodyweight, 1)
        if relative_total >= 7:
            strength_desc = "elite-level totals"
        elif relative_total >= 5.5:
            strength_desc = "advanced totals approaching competition-level"
        elif relative_total >= 4:
            strength_desc = "solid intermediate totals with room for growth"
        elif relative_total >= 2.5:
            strength_desc = "novice totals — building the foundation"
        else:
            strength_desc = "beginner totals — focusing on technique first"
    else:
        strength_desc = "no recorded maxes — start conservative"

    # ── Week phase descriptions ──
    week_phases = {
        1: ("Volume Accumulation", "Build work capacity. Moderate intensity (75-82% 1RM for compounds). Higher rep ranges. Establish movement patterns and build a fatigue base."),
        2: ("Intensification", "Increase load, reduce volume slightly. Working sets at 82-88% 1RM. Introduce heavier singles/doubles on main lifts if experience allows."),
        3: ("Peaking / Overreach", "Highest intensity of the block (88-95% 1RM on main lifts). Lowest volume. Heavy doubles and singles. This week should feel HARD."),
        4: ("Deload / Recovery", "Reduce ALL loads to 55-65% of max. Cut volume by 40-50%. Focus on movement quality, mobility, and active recovery. The body rebuilds here."),
    }
    phase_name, phase_desc = week_phases.get(target_week, ("Training", "Standard training week."))

    # ── Build JSON schema ──
    if target_week == 1:
        json_schema = f"""JSON SCHEMA REQUIREMENTS (OUTPUT AS VALID JSON — NO MARKDOWN FENCES):
- Root object must contain: "summary" (string, 1-2 sentences describing this SPECIFIC athlete's program), "goal" (string), "training_days" (integer), "weak_point" (string), "experience_level" (string), "week" (integer 1), "focus" (string), "diet" (object), "tips" (array of exactly 4 strings), and keys for each training day: "day1_ex", "day2_ex" ... up to "day{days}_ex".
- Each "dayX_ex" must be an array of exercise objects.
- Each exercise object must contain: "name" (string, concise e.g. "Squat" not "High-Bar Back Squat"), "sets" (integer), "reps" (string like "5" or "3-5" or "8-10"), "weight" (integer in kg), "rpe" (number, can be decimal like 7.5), "rest" (string like "2-3 min" or "60-90s"), "notes" (string, 1 brief coaching cue).
- The "diet" object must contain: "calories": {calories}, "protein": {protein}, "carbs": {carbs}, "fats": {fats}, "maintenance": {int(maintenance)}, "tdee": {int(tdee)}.

CRITICAL: Return ONLY Week 1 data. Do NOT return all 4 weeks."""
    else:
        json_schema = f"""JSON SCHEMA REQUIREMENTS (OUTPUT AS VALID JSON — NO MARKDOWN FENCES):
- Root object must contain: "week" (integer {target_week}), "focus" (string), and keys for each training day: "day1_ex", "day2_ex" ... up to "day{days}_ex".
- Each "dayX_ex" must be an array of exercise objects.
- Each exercise object must contain: "name" (string, concise), "sets" (integer), "reps" (string), "weight" (integer in kg), "rpe" (number, can be decimal), "rest" (string), "notes" (string, 1 brief coaching cue).

CRITICAL: Return ONLY Week {target_week}. Do NOT return all 4 weeks."""

    # ── Assemble the mega-prompt ──
    prompt = f"""You are an ELITE Powerlifting AI Coach with 20+ years of experience coaching athletes from beginners to IPF World Championship competitors. You think like a real coach — not a template generator.

Your task: Design Week {target_week} ("{phase_name}") of a 4-week {days}-day training block.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATHLETE DOSSIER (read this like a coach meeting their athlete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Gender: {gender}
- Age: {age} years old
- Bodyweight: {bodyweight} kg
- Height: {height} cm
- Training Experience: {years_training} years ({exp["tier"]} tier)
- Current Maxes: Squat {squat}kg | Bench {bench}kg | Deadlift {deadlift}kg
- Total: {total}kg ({strength_desc})
- Identified Weak Points: {weak_points_str}
- Primary Goal: {goal}
- Training Frequency: {days} days/week
- Activity Level: {activity}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXPERIENCE-BASED COACHING DIRECTIVES ({exp["tier"]} — {exp["exercise_complexity"]} complexity)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{exp["directives"]}
- Periodization approach: {exp["periodization"]}
- Target RPE range for this experience level: {exp["rpe_range"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOAL-SPECIFIC TRAINING PARAMETERS ("{goal}")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Primary Rep Range: {goal_params["rep_range"]}
- Intensity Zone: {goal_params["intensity_range"]}
- Volume Level: {goal_params["volume_level"]}
- Target Frequency: {goal_params["frequency"]}
- Rest Periods: {goal_params["rest_periods"]}
- Exercises Per Session: {goal_params["exercise_count_per_day"]}
- RPE Ceiling: {goal_params["rpe_ceiling"]}
- Working Sets Range: {goal_params["set_range"]} sets per exercise
{goal_params["special_instructions"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEEK {target_week} PHASE: {phase_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{phase_desc}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY COACHING RULES (violating these = program failure)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. WEIGHTS MUST BE CALCULATED from the athlete's actual maxes:
   - Squat working weights derived from {squat}kg max
   - Bench working weights derived from {bench}kg max
   - Deadlift working weights derived from {deadlift}kg max
   - Round all weights to nearest 2.5kg
   - If a max is 0, substitute bodyweight-appropriate alternatives

2. RPE MUST VARY across the session:
   - Main compound lifts: Higher RPE ({exp["rpe_range"]})
   - Accessory work: RPE 6-7.5 (leaving reps in reserve)
   - Warm-up/mobility: RPE 4-5
   - NEVER assign RPE 10 unless it's a true max-effort test day
   - RPE should PROGRESS across weeks: W1 lower → W3 highest → W4 lowest

3. INTENSITY MUST VARY across days within the same week:
   - Day 1 might be heavy squats at 85% → Day 2 light bench volume at 72%
   - NOT every day at the same percentage
   - At least one "lighter" day per week focused on technique/volume

4. EXERCISE COUNT MUST VARY by day type:
   - Heavy squat or deadlift day: 3-4 exercises (CNS fatigue is real)
   - Bench or upper body day: 5-6 exercises
   - Accessory/hypertrophy day: 5-7 exercises
   - NEVER make every day the same length

5. EXERCISE SELECTION must match the {exp["tier"]} experience level:
   - Complexity ceiling: {exp["exercise_complexity"]}
   - Must include weak-point targeted accessories for: {weak_points_str}

6. Each exercise "notes" field should contain ONE specific coaching cue
   (e.g., "Drive knees out", "Pause 1s at chest", "Control the eccentric 3s")

7. "tips" array (Week 1 only): Provide 4 genuinely useful, personalized tips
   that reference THIS athlete's specific stats, goals, and weak points.
   NOT generic advice like "stay hydrated" — real coaching insights.

{json_schema}
"""
    return prompt