"""
Smart builder - creates varied, coach-like programs
Supports: Build Strength, Bulk, Cut, Powerbuilding
"""

def _guess_day_label(exercises, default_label):
    if not exercises:
        return default_label
    
    lifts = [str(ex.get("name", "")).lower() for ex in exercises if isinstance(ex, dict)]
    text = " ".join(lifts)
    
    # Try the first heavy lift first
    for ex_name in lifts:
        if "squat" in ex_name: return "Squat Focus"
        if "deadlift" in ex_name or "rdl" in ex_name: return "Deadlift Focus"
        if "bench" in ex_name: return "Bench Focus"
        if "overhead press" in ex_name or "ohp" in ex_name: return "Overhead Press Focus"
        
    # If not in the first few, check overall
    if "squat" in text: return "Lower Body (Squat)"
    if "deadlift" in text: return "Lower Body (Deadlift)"
    if "bench" in text or "press" in text: return "Upper Body (Push)"
    if "curl" in text or "row" in text: return "Upper Body (Pull)"
    
    return default_label

def expand_minimal_json(minimal_data, days):
    """Build exercises cleanly back to dashboard format"""

    weeks = minimal_data.get("weeks", [])
    goal = minimal_data.get("goal", "Build Strength")

    # Strategic day label templates (varies by week AND goal)
    day_labels = _get_day_labels(goal)

    for week in weeks:
        week_num = week.get("week", 1)
        full_days = []
        labels = day_labels.get(week_num, {}).get(days, [f"Day {i+1}" for i in range(days)])

        existing_days = week.get("days")
        if isinstance(existing_days, list) and len(existing_days) > 0 and isinstance(existing_days[0], dict) and existing_days[0].get("exercises"):
            # Ensure the AI's provided labels are accurate to the content
            for idx, d_obj in enumerate(existing_days):
                if isinstance(d_obj, dict):
                    curr_label = d_obj.get("label", f"Day {idx+1}")
                    d_obj["label"] = _guess_day_label(d_obj.get("exercises", []), curr_label)
        else:
            for i in range(1, days + 1):
                # Aggressively extract exercises despite AI hallucinations
                exercises = []
                for key_guess in [f"day{i}_ex", f"day{i}", f"day_{i}", f"day {i}", f"day0{i}", f"day_{i}_exercises"]:
                    for k, v in week.items():
                        if str(k).lower() == key_guess:
                            exercises = v
                            break
                    if exercises:
                        break
                
                # Fallback: find any remaining list containing 'day' and the day number
                if not exercises:
                    for k, v in week.items():
                        if isinstance(v, list) and k not in ["tips", "days", "weeks"] and str(i) in str(k) and "day" in str(k).lower():
                            exercises = v
                            break

                # Unwrap if the AI nested them inside another object like {"day1": {"exercises": [...]}}
                if isinstance(exercises, dict):
                    exercises = exercises.get("exercises", exercises.get("workout", []))

                if not isinstance(exercises, list):
                    if exercises:
                        exercises = [exercises]
                    else:
                        exercises = []

                # Use dynamic labels based on what the AI actually generated
                base_label = labels[i-1] if i-1 < len(labels) else f"Day {i}"
                label = _guess_day_label(exercises, base_label)

                full_days.append({
                    "day_number": i,
                    "label": label,
                    "exercises": exercises
                })

            week["days"] = full_days

        for key in list(week.keys()):
            # Clear out raw day keys to simplify the object
            if str(key).lower().startswith("day") and key != "days":
                del week[key]

    return minimal_data


def _get_day_labels(goal):
    """Return day label templates based on goal type."""
    
    if goal == "Powerbuilding":
        return {
            1: {
                6: ["Heavy Squat + Quad Hypertrophy", "Heavy Bench + Chest/Triceps", "Heavy Deadlift + Back", "Upper Hypertrophy", "Lower Hypertrophy", "Arms & Shoulders"],
                5: ["Heavy Squat + Legs", "Heavy Bench + Push", "Heavy Deadlift + Pull", "Upper Hypertrophy", "Lower Hypertrophy"],
                4: ["Heavy Squat + Quads", "Heavy Bench + Push", "Heavy Deadlift + Pull", "Hypertrophy Day"],
                3: ["Heavy Squat + Legs", "Heavy Bench + Upper", "Heavy Deadlift + Back"]
            },
            2: {
                6: ["Squat Intensity + Accessories", "Bench Intensity + Chest", "Deadlift Intensity + Back", "Push Hypertrophy", "Pull Hypertrophy", "Weak Points"],
                5: ["Squat Intensity", "Bench Intensity + Push", "Deadlift Intensity + Pull", "Upper Volume", "Lower Volume"],
                4: ["Squat Intensity", "Bench Intensity + Push", "Deadlift Intensity + Pull", "Full Body Volume"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity"]
            },
            3: {
                6: ["Squat Peak + Pump", "Bench Peak + Pump", "Deadlift Peak + Pump", "Upper Body Builder", "Lower Body Builder", "Active Recovery"],
                5: ["Squat Peak", "Bench Peak + Push", "Deadlift Peak + Pull", "Hypertrophy Upper", "Hypertrophy Lower"],
                4: ["Squat Peak", "Bench Peak", "Deadlift Peak", "Full Body Pump"],
                3: ["Squat Peak", "Bench Peak", "Deadlift Peak"]
            },
            4: {
                6: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core", "Light Pump Session", "Active Recovery", "Full Rest"],
                5: ["Light Squat & Mobility", "Light Bench", "Light Deadlift", "Light Accessories", "Full Rest"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Full Rest"],
                3: ["Light Squat", "Light Bench", "Light Deadlift"]
            }
        }
    elif goal == "Cut":
        return {
            1: {
                6: ["Heavy Squat + Metabolic", "Heavy Bench + Supersets", "Heavy Deadlift + Circuit", "Upper Body Maintenance", "Lower Body Maintenance", "Active Recovery"],
                5: ["Heavy Squat + Metabolic", "Heavy Bench + Supersets", "Deadlift + Posterior", "Upper Maintenance", "Conditioning"],
                4: ["Heavy Squat", "Heavy Bench + Back", "Heavy Deadlift", "Metabolic Conditioning"],
                3: ["Heavy Squat", "Heavy Bench", "Heavy Deadlift"]
            },
            2: {
                6: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Upper Supersets", "Lower Supersets", "Active Recovery"],
                5: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Full Body Supersets", "Conditioning"],
                4: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Conditioning"],
                3: ["Squat Volume", "Bench Volume", "Deadlift Volume"]
            },
            3: {
                6: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Upper Maintenance", "Metabolic Finisher", "Light Mobility"],
                5: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Full Body", "Active Recovery"],
                4: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Deload"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity"]
            },
            4: {
                6: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core", "Light Cardio", "Active Recovery", "Full Rest"],
                5: ["Light Squat", "Light Bench", "Light Deadlift", "Active Recovery", "Full Rest"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Full Rest"],
                3: ["Light Squat", "Light Bench", "Light Deadlift"]
            }
        }
    else:
        # Build Strength & Bulk share similar structure
        return {
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
