"""
Smart builder - creates varied, coach-like programs
"""

def expand_minimal_json(minimal_data, days):
    """Build exercises with strategic day labels and varied structure"""
    
    weeks = minimal_data.get("weeks", [])
    weak_point = minimal_data.get("weak_point", "balanced")
    
    # Strategic day label templates (varies by week)
    day_labels = {
        1: {
            6: ["Heavy Squat Focus", "Heavy Bench & Back", "Moderate Deadlift & Posterior", "Active Recovery & Mobility", "Heavy Deadlift Focus", "Bench Volume & Accessories"],
            5: ["Heavy Squat Focus", "Heavy Bench & Back", "Deadlift & Posterior", "Speed & Volume", "Bench Hypertrophy"],
            4: ["Heavy Squat", "Heavy Bench & Back", "Heavy Deadlift", "Speed & Accessories"],
            3: ["Heavy Squat", "Heavy Bench", "Heavy Deadlift"]
        },
        2: {
            6: ["Deadlift Focus", "Squat Heavy", "Bench Heavy", "Recovery Day", "Volume Squat", "Upper Body Accessories"],
            5: ["Deadlift Heavy", "Bench Heavy", "Squat Volume", "Speed Work", "Recovery & Mobility"],
            4: ["Deadlift Heavy", "Bench Heavy", "Squat Heavy", "Volume Day"],
            3: ["Deadlift Heavy", "Bench Heavy", "Squat Heavy"]
        },
        3: {
            6: ["Bench Peak", "Deadlift Peak", "Squat Peak", "Active Recovery", "Accessory Work", "Light Mobility"],
            5: ["Bench Peak", "Squat Peak", "Deadlift Peak", "Speed Work", "Light Accessories"],
            4: ["Bench Peak", "Deadlift Peak", "Squat Peak", "Deload"],
            3: ["Heavy Max Effort", "Heavy Max Effort", "Heavy Max Effort"]
        },
        4: {
            6: ["Light Squat & Mobility", "Light Bench & Upper Body", "Light Deadlift & Core", "Full Rest", "Full Rest", "Active Recovery & Stretching"],
            5: ["Light Squat & Mobility", "Light Bench", "Light Deadlift", "Active Recovery", "Full Rest"],
            4: ["Light Squat", "Light Bench", "Light Deadlift", "Full Rest"],
            3: ["Light Squat", "Light Bench", "Light Deadlift"]
        }
    }
    
    for week in weeks:
        week_num = week.get("week", 1)
        full_days = []
        
        try:
            squat_w = int(float(week.get("day1_ex", [{}])[0].get("weight", 100)))
            bench_w = int(float(week.get("day2_ex", [{}])[0].get("weight", 70)))
            dl_w = int(float(week.get("day3_ex", [{}])[0].get("weight", 130)))
        except (ValueError, IndexError, TypeError):
            squat_w, bench_w, dl_w = 100, 70, 130
        
        # Get strategic labels for this week
        labels = day_labels.get(week_num, {}).get(days, [f"Day {i+1}" for i in range(days)])
        
        # DAY 1
        if days >= 1:
            exercises = [
                {"name": "Back Squat", "sets": 5, "reps": "5", "weight": squat_w, "rpe": 6, "note": "Main lift - focus on depth and form"},
                {"name": "Pause Squats", "sets": 3, "reps": "5", "weight": int(squat_w * 0.85), "rpe": 6, "note": "2-second pause - technique work"},
                {"name": "Leg Press", "sets": 3, "reps": "8", "weight": int(squat_w * 1.8), "rpe": 6, "note": "Quad volume - full range"},
                {"name": "Leg Curls", "sets": 3, "reps": "10", "weight": int(squat_w * 0.35), "rpe": 5, "note": "Posterior chain balance"},
            ]
            full_days.append({"day_number": 1, "label": labels[0], "exercises": exercises})
        
        # DAY 2
        if days >= 2:
            exercises = [
                {"name": "Bench Press", "sets": 5, "reps": "5", "weight": bench_w, "rpe": 6, "note": "Main lift - controlled descent"},
                {"name": "Barbell Rows", "sets": 3, "reps": "5", "weight": int(dl_w * 0.65), "rpe": 7, "note": "Back balance - critical for shoulders"},
                {"name": "Close Grip Bench", "sets": 3, "reps": "6", "weight": int(bench_w * 0.88), "rpe": 6, "note": "Tricep emphasis"},
                {"name": "Tricep Pushdowns", "sets": 3, "reps": "10", "weight": int(bench_w * 0.40), "rpe": 5, "note": "Isolation work"},
                {"name": "Face Pulls", "sets": 3, "reps": "12", "weight": int(bench_w * 0.25), "rpe": 4, "note": "Shoulder health"},
            ]
            full_days.append({"day_number": 2, "label": labels[1], "exercises": exercises})
        
        # DAY 3
        if days >= 3:
            exercises = [
                {"name": "Deadlifts", "sets": 5, "reps": "5", "weight": dl_w, "rpe": 6, "note": "Main lift - explosive drive"},
                {"name": "Barbell Rows", "sets": 3, "reps": "5", "weight": int(dl_w * 0.65), "rpe": 7, "note": "Back thickness"},
                {"name": "Rack Pulls", "sets": 3, "reps": "5", "weight": int(dl_w * 1.10), "rpe": 7, "note": "Lockout strength"},
                {"name": "Good Mornings", "sets": 3, "reps": "8", "weight": int(dl_w * 0.50), "rpe": 6, "note": "Lower back"},
                {"name": "RDL", "sets": 3, "reps": "8", "weight": int(dl_w * 0.65), "rpe": 5, "note": "Hamstring strength"},
            ]
            full_days.append({"day_number": 3, "label": labels[2], "exercises": exercises})
        
        # DAY 4
        if days >= 4:
            exercises = [
                {"name": "Speed Bench", "sets": 6, "reps": "3", "weight": int(bench_w * 0.60), "rpe": 5, "note": "Explosive - focus on speed"},
                {"name": "Barbell Rows", "sets": 3, "reps": "8", "weight": int(dl_w * 0.60), "rpe": 6, "note": "Volume back work"},
                {"name": "Incline DB Press", "sets": 3, "reps": "8", "weight": int(bench_w * 0.35), "rpe": 6, "note": "Upper chest emphasis"},
                {"name": "Dumbbell Rows", "sets": 3, "reps": "8", "weight": int(bench_w * 0.40), "rpe": 6, "note": "Unilateral back"},
                {"name": "OHP", "sets": 3, "reps": "6", "weight": int(bench_w * 0.55), "rpe": 6, "note": "Shoulder strength"},
            ]
            full_days.append({"day_number": 4, "label": labels[3], "exercises": exercises})
        
        # DAY 5
        if days >= 5:
            exercises = [
                {"name": "Box Squats", "sets": 3, "reps": "6", "weight": int(squat_w * 0.75), "rpe": 6, "note": "Bottom position work"},
                {"name": "Belt Squat", "sets": 3, "reps": "10", "weight": int(squat_w * 0.90), "rpe": 6, "note": "High rep volume"},
                {"name": "Chest-Supported Rows", "sets": 3, "reps": "8", "weight": int(dl_w * 0.60), "rpe": 6, "note": "Back hypertrophy"},
                {"name": "Leg Extensions", "sets": 3, "reps": "12", "weight": int(squat_w * 0.35), "rpe": 5, "note": "Quad isolation"},
                {"name": "Lying Leg Curls", "sets": 3, "reps": "10", "weight": int(squat_w * 0.40), "rpe": 5, "note": "Hamstring volume"},
            ]
            full_days.append({"day_number": 5, "label": labels[4], "exercises": exercises})
        
        # DAY 6
        if days >= 6:
            exercises = [
                {"name": "Incline DB Bench", "sets": 3, "reps": "10", "weight": int(bench_w * 0.32), "rpe": 5, "note": "Upper chest pump"},
                {"name": "Machine Leg Press", "sets": 3, "reps": "12", "weight": int(squat_w * 1.7), "rpe": 5, "note": "Controlled quad work"},
                {"name": "Seal Rows", "sets": 3, "reps": "10", "weight": int(dl_w * 0.55), "rpe": 5, "note": "Light back work"},
                {"name": "Dumbbell Rows", "sets": 3, "reps": "8", "weight": int(bench_w * 0.35), "rpe": 5, "note": "Unilateral back"},
                {"name": "Lateral Raises", "sets": 3, "reps": "12", "weight": int(bench_w * 0.15), "rpe": 4, "note": "Shoulder isolation"},
            ]
            full_days.append({"day_number": 6, "label": labels[5], "exercises": exercises})
        
        week["days"] = full_days
        for key in list(week.keys()):
            if key.startswith("day") and key.endswith("_ex"):
                del week[key]
    
    return minimal_data