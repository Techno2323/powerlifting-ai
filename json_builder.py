"""
Smart builder - creates varied, coach-like programs
"""

def expand_minimal_json(minimal_data, days):
    """Build exercises cleanly back to dashboard format"""
    
    weeks = minimal_data.get("weeks", [])
    
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
        labels = day_labels.get(week_num, {}).get(days, [f"Day {i+1}" for i in range(days)])
        
        for i in range(1, days + 1):
            ex_key = f"day{i}_ex"
            exercises = week.get(ex_key, [])
            label = labels[i-1] if i-1 < len(labels) else f"Day {i}"
            
            full_days.append({
                "day_number": i, 
                "label": label, 
                "exercises": exercises
            })
        
        week["days"] = full_days
        for key in list(week.keys()):
            if key.startswith("day") and key.endswith("_ex"):
                del week[key]
                
    return minimal_data