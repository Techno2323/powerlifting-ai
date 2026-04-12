# json_builder.py - Nippard-Inspired Program Builder

def _guess_day_label(exercises, default_label):
    if not exercises:
        return default_label

    lifts = [str(ex.get("name", "")).lower() for ex in exercises if isinstance(ex, dict)]
    types = [str(ex.get("type", "")).lower() for ex in exercises if isinstance(ex, dict)]

    # Check for primary top sets first — these define the day
    primary_exercises = [
        ex for ex in exercises
        if isinstance(ex, dict) and "primary" in str(ex.get("type", "")).lower()
    ]

    if primary_exercises:
        primary_name = primary_exercises[0].get("name", "").lower()
        if "squat" in primary_name:
            return "Squat Focus"
        if "deadlift" in primary_name or "block pull" in primary_name or "rack pull" in primary_name:
            return "Deadlift Focus"
        if "bench" in primary_name:
            return "Bench Focus"
        if "overhead" in primary_name or "ohp" in primary_name or "press" in primary_name:
            return "Overhead Press Focus"

    # Fallback: scan all exercise names
    text = " ".join(lifts)
    for name in lifts:
        if "squat" in name: return "Squat Focus"
        if "deadlift" in name or "block pull" in name: return "Deadlift Focus"
        if "bench" in name: return "Bench Focus"
        if "overhead" in name or "ohp" in name: return "Overhead Press Focus"

    if "curl" in text or "row" in text or "pulldown" in text: return "Upper Body Pull"
    if "press" in text or "dip" in text: return "Upper Body Push"
    if "leg" in text or "lunge" in text: return "Lower Body"
    if "arm" in text or "lateral" in text: return "Arms & Accessories"

    return default_label


def _get_day_labels(goal, days):
    """
    Returns intelligent day label templates based on Nippard's programming philosophy.
    Odd weeks (1, 3) = strength focus. Even weeks (2, 4) = hypertrophy/deload focus.
    """
    if goal == "Powerbuilding":
        templates = {
            3: {
                1: ["Heavy Squat + Accessories", "Heavy Bench + Upper Hypertrophy", "Heavy Deadlift + Back Volume"],
                2: ["Lower Hypertrophy + Deadlift", "Upper Hypertrophy + Bench", "Full Body Technique"],
                3: ["Heavy Squat Peak", "Heavy Bench Peak", "Heavy Deadlift Peak"],
                4: ["Light Squat + Mobility", "Light Bench + Upper", "Light Deadlift + Core"],
            },
            4: {
                1: ["Heavy Squat + Quad Work", "Heavy Bench + Push", "Heavy Deadlift + Pull", "Hypertrophy Day"],
                2: ["Lower Volume + Deadlift", "Upper Volume + Bench", "Lower Accessories", "Upper Accessories"],
                3: ["Squat Peak + Pump", "Bench Peak + Pump", "Deadlift Peak + Pump", "Full Body Pump"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Active Recovery"],
            },
            5: {
                1: ["Heavy Squat + Legs", "Heavy Bench + Push", "Heavy Deadlift + Pull", "Upper Hypertrophy", "Lower Hypertrophy"],
                2: ["Lower Volume", "Upper Volume", "Deadlift Variation", "Push Hypertrophy", "Pull Hypertrophy"],
                3: ["Squat Peak", "Bench Peak", "Deadlift Peak", "Upper Body Builder", "Lower Body Builder"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Light Accessories", "Active Recovery"],
            },
            6: {
                1: ["Heavy Squat + Quad Hypertrophy", "Heavy Bench + Chest/Triceps", "Heavy Deadlift + Back", "Upper Hypertrophy", "Lower Hypertrophy", "Arms & Shoulders"],
                2: ["Squat Volume + Accessories", "Bench Volume + Accessories", "Deadlift Volume + Back", "Push Hypertrophy", "Pull Hypertrophy", "Weak Points"],
                3: ["Squat Peak + Pump", "Bench Peak + Pump", "Deadlift Peak + Pump", "Upper Builder", "Lower Builder", "Active Recovery"],
                4: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core", "Light Pump", "Active Recovery", "Full Rest"],
            }
        }
    elif goal == "Cut":
        templates = {
            3: {
                1: ["Heavy Squat + Metabolic", "Heavy Bench + Supersets", "Heavy Deadlift + Circuit"],
                2: ["Squat Volume + Conditioning", "Bench Volume + Supersets", "Deadlift + Posterior Chain"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity"],
                4: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core"],
            },
            4: {
                1: ["Heavy Squat", "Heavy Bench + Back", "Heavy Deadlift", "Metabolic Conditioning"],
                2: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Full Body Circuit"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Conditioning"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Active Recovery"],
            },
            5: {
                1: ["Heavy Squat + Metabolic", "Heavy Bench + Supersets", "Deadlift + Posterior", "Upper Maintenance", "Conditioning"],
                2: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Upper Supersets", "Lower Supersets"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Full Body", "Active Recovery"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Active Recovery", "Full Rest"],
            },
            6: {
                1: ["Heavy Squat + Metabolic", "Heavy Bench + Supersets", "Heavy Deadlift + Circuit", "Upper Maintenance", "Lower Maintenance", "Active Recovery"],
                2: ["Squat Volume", "Bench Volume", "Deadlift Volume", "Upper Supersets", "Lower Supersets", "Active Recovery"],
                3: ["Squat Intensity", "Bench Intensity", "Deadlift Intensity", "Upper Maintenance", "Metabolic Finisher", "Light Mobility"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Light Cardio", "Active Recovery", "Full Rest"],
            }
        }
    else:
        # Build Strength & Bulk — Nippard odd/even week style
        templates = {
            3: {
                1: ["Heavy Squat + Accessories", "Heavy Bench & Back", "Deadlift & Posterior Chain"],
                2: ["Deadlift Focus + Lower Volume", "Bench Focus + Upper Volume", "Squat Volume + Accessories"],
                3: ["Squat Peak", "Bench Peak", "Deadlift Peak"],
                4: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core"],
            },
            4: {
                1: ["Heavy Squat", "Heavy Bench & Back", "Heavy Deadlift", "Speed & Volume Day"],
                2: ["Deadlift Heavy", "Bench Heavy", "Squat Heavy", "Volume & Accessories"],
                3: ["Squat Peak", "Bench Peak", "Deadlift Peak", "Active Recovery"],
                4: ["Light Squat", "Light Bench", "Light Deadlift", "Full Rest"],
            },
            5: {
                1: ["Heavy Squat Focus", "Heavy Bench & Back", "Deadlift & Posterior", "Speed & Volume", "Bench Hypertrophy"],
                2: ["Deadlift Heavy", "Bench Heavy", "Squat Volume", "Speed Work", "Recovery & Mobility"],
                3: ["Bench Peak", "Squat Peak", "Deadlift Peak", "Speed Work", "Light Accessories"],
                4: ["Light Squat & Mobility", "Light Bench", "Light Deadlift", "Active Recovery", "Full Rest"],
            },
            6: {
                1: ["Heavy Squat Focus", "Heavy Bench & Back", "Moderate Deadlift & Posterior", "Active Recovery", "Heavy Deadlift Focus", "Bench Volume & Accessories"],
                2: ["Deadlift Heavy", "Squat Heavy", "Bench Heavy", "Recovery Day", "Volume Squat", "Upper Accessories"],
                3: ["Bench Peak", "Deadlift Peak", "Squat Peak", "Active Recovery", "Accessory Work", "Light Mobility"],
                4: ["Light Squat & Mobility", "Light Bench & Upper", "Light Deadlift & Core", "Full Rest", "Full Rest", "Active Recovery"],
            }
        }

    day_template = templates.get(days, templates.get(4, {}))
    return day_template


def expand_minimal_json(minimal_data, days):
    """
    Converts AI-generated JSON into full dashboard-compatible format.
    Handles Nippard-style top set + back-off set structure.
    """
    weeks = minimal_data.get("weeks", [])
    goal = minimal_data.get("goal", "Build Strength")
    day_templates = _get_day_labels(goal, days)

    for week in weeks:
        week_num = week.get("week", 1)
        labels = day_templates.get(week_num, [f"Day {i+1}" for i in range(days)])
        full_days = []

        existing_days = week.get("days")
        if (isinstance(existing_days, list) and
                len(existing_days) > 0 and
                isinstance(existing_days[0], dict) and
                existing_days[0].get("exercises")):
            # Days already structured correctly — just fix labels
            for idx, d_obj in enumerate(existing_days):
                if isinstance(d_obj, dict):
                    curr_label = d_obj.get("label", f"Day {idx + 1}")
                    d_obj["label"] = _guess_day_label(d_obj.get("exercises", []), curr_label)
                    # Ensure day_number exists
                    if "day_number" not in d_obj:
                        d_obj["day_number"] = idx + 1
        else:
            # Extract from flat dayX_ex structure
            for i in range(1, days + 1):
                exercises = []

                # Try multiple key formats
                key_guesses = [
                    f"day{i}_ex", f"day{i}", f"day_{i}",
                    f"day {i}", f"day0{i}", f"day_{i}_exercises",
                    f"Day{i}", f"Day {i}"
                ]
                for key_guess in key_guesses:
                    for k, v in week.items():
                        if str(k).lower() == key_guess.lower():
                            exercises = v
                            break
                    if exercises:
                        break

                # Fallback: find any remaining list with day number
                if not exercises:
                    for k, v in week.items():
                        if (isinstance(v, list) and
                                k not in ["tips", "days", "weeks", "meals"] and
                                str(i) in str(k) and
                                "day" in str(k).lower()):
                            exercises = v
                            break

                # Unwrap nested structure
                if isinstance(exercises, dict):
                    exercises = exercises.get("exercises",
                               exercises.get("workout",
                               exercises.get("sets", [])))

                if not isinstance(exercises, list):
                    exercises = [exercises] if exercises else []

                # Sort exercises by type: primary_top first, then backoff, then secondary, tertiary, circuit
                type_order = {
                    "primary_top": 0,
                    "primary_backoff": 1,
                    "secondary": 2,
                    "tertiary": 3,
                    "circuit_a1": 4,
                    "circuit_a2": 4,
                    "circuit_b1": 5,
                    "circuit_b2": 5,
                }
                exercises_sorted = sorted(
                    exercises,
                    key=lambda x: type_order.get(
                        str(x.get("type", "tertiary")).lower().replace("/", "_").replace(" ", "_"),
                        3
                    ) if isinstance(x, dict) else 3
                )

                base_label = labels[i - 1] if i - 1 < len(labels) else f"Day {i}"
                label = _guess_day_label(exercises_sorted, base_label)

                full_days.append({
                    "day_number": i,
                    "label": label,
                    "exercises": exercises_sorted
                })

            week["days"] = full_days

        # Clean up flat day keys
        keys_to_remove = [
            k for k in list(week.keys())
            if str(k).lower().startswith("day") and k != "days"
        ]
        for k in keys_to_remove:
            del week[k]

    return minimal_data