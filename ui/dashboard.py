import json
import re
import streamlit as st
import pandas as pd
from datetime import date
from database import save_log_entry, archive_plan, delete_plan
from utils import build_session_schedule, get_today_session, calculate_progress, calculate_score

GLOSSARY = {
    "rpe": "RPE = Rate of Perceived Exertion. Scale 1-10. RPE 7 = 3 reps left in tank. RPE 8 = 2 reps. RPE 9 = 1 rep. RPE 10 = absolute max.",
    "sets": "Sets = how many times you repeat a group of reps. 3 sets means do the exercise 3 times with rest in between.",
    "reps": "Reps = Repetitions. How many times you lift in one set.",
    "rdl": "RDL = Romanian Deadlift. Hinge at hips with slight knee bend. Great for hamstrings.",
    "ohp": "OHP = Overhead Press. Press barbell from shoulders straight overhead.",
    "amrap": "AMRAP = As Many Reps As Possible. Do as many reps as you can with good form.",
    "deload": "Deload = A lighter week to let your body recover and come back stronger.",
}

_DAY_KEY_RE = re.compile(r"^day[_ ]?(\d+)(?:_.*)?$", re.IGNORECASE)


def _to_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return [value]


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_exercise(ex):
    if isinstance(ex, dict):
        return {
            "name": ex.get("name") or ex.get("exercise") or ex.get("movement") or "Exercise",
            "sets": ex.get("sets", ex.get("set", "?")),
            "reps": ex.get("reps", ex.get("rep", ex.get("range", "?"))),
            "weight": ex.get("weight", ex.get("load", ex.get("kg", "?"))),
            "rpe": ex.get("rpe", ex.get("intensity", "?")),
            "note": ex.get("note", ex.get("notes", ex.get("cue", ""))),
        }
    if isinstance(ex, str):
        return {
            "name": ex,
            "sets": "?",
            "reps": "?",
            "weight": "?",
            "rpe": "?",
            "note": "",
        }
    return {
        "name": "Exercise",
        "sets": "?",
        "reps": "?",
        "weight": "?",
        "rpe": "?",
        "note": "",
    }


def _normalize_day(day_data, default_day_number):
    if isinstance(day_data, dict):
        day_number = _safe_int(
            day_data.get("day_number", day_data.get("day", default_day_number)),
            default_day_number,
        )
        label = day_data.get("label") or day_data.get("name") or f"Day {day_number}"

        raw_exercises = day_data.get("exercises")
        if raw_exercises is None:
            raw_exercises = day_data.get("workout")
        if raw_exercises is None:
            raw_exercises = day_data.get("movements")

        if raw_exercises is None:
            day_key_entries = sorted(
                (
                    (_safe_int(match.group(1), 0), value)
                    for key, value in day_data.items()
                    for match in [_DAY_KEY_RE.match(str(key))]
                    if match
                ),
                key=lambda item: item[0],
            )
            if day_key_entries:
                merged = []
                for _, day_items in day_key_entries:
                    merged.extend(_to_list(day_items))
                raw_exercises = merged

        exercises = [_normalize_exercise(ex) for ex in _to_list(raw_exercises)]
        return {
            "day_number": day_number,
            "label": label,
            "exercises": exercises,
        }

    if isinstance(day_data, list):
        exercises = [_normalize_exercise(ex) for ex in day_data]
        return {
            "day_number": default_day_number,
            "label": f"Day {default_day_number}",
            "exercises": exercises,
        }

    return {
        "day_number": default_day_number,
        "label": f"Day {default_day_number}",
        "exercises": [],
    }


def _extract_days_from_week(week_data):
    if not isinstance(week_data, dict):
        return _to_list(week_data)

    raw_days = week_data.get("days")
    if raw_days is None:
        raw_days = week_data.get("sessions")
    if raw_days is None:
        raw_days = week_data.get("workouts")
    if raw_days is not None:
        return _to_list(raw_days)

    day_key_entries = sorted(
        (
            (_safe_int(match.group(1), 0), value)
            for key, value in week_data.items()
            for match in [_DAY_KEY_RE.match(str(key))]
            if match
        ),
        key=lambda item: item[0],
    )
    if day_key_entries:
        return [
            {
                "day_number": day_number,
                "label": f"Day {day_number}",
                "exercises": day_items,
            }
            for day_number, day_items in day_key_entries
        ]

    return []


def _coerce_plan_dict(plan_payload):
    if isinstance(plan_payload, dict):
        return plan_payload
    if isinstance(plan_payload, str):
        try:
            parsed = json.loads(plan_payload)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}


def _normalize_plan(plan_payload):
    plan = _coerce_plan_dict(plan_payload)
    if not plan:
        return {"weeks": [], "diet": {}, "tips": [], "training_days": 3}

    nested_program = _coerce_plan_dict(plan.get("program"))
    root = nested_program if nested_program else plan

    weeks_raw = root.get("weeks")
    week_items = []
    if isinstance(weeks_raw, dict):
        def _week_sort_key(key):
            match = re.search(r"\d+", str(key))
            return int(match.group()) if match else 9999

        for key in sorted(weeks_raw.keys(), key=_week_sort_key):
            week_items.append(weeks_raw[key])
    elif isinstance(weeks_raw, list):
        week_items = weeks_raw

    if not week_items:
        if root.get("days") is not None:
            week_items = [{
                "week": root.get("week", 1),
                "focus": root.get("focus", "Training Program"),
                "days": root.get("days", []),
            }]
        else:
            top_day_keys = sorted(
                (
                    (_safe_int(match.group(1), 0), value)
                    for key, value in root.items()
                    for match in [_DAY_KEY_RE.match(str(key))]
                    if match
                ),
                key=lambda item: item[0],
            )
            if top_day_keys:
                week_obj = {
                    "week": root.get("week", 1),
                    "focus": root.get("focus", "Training Program"),
                }
                for day_number, day_items in top_day_keys:
                    week_obj[f"day{day_number}_ex"] = day_items
                week_items = [week_obj]

    normalized_weeks = []
    for idx, week_data in enumerate(week_items, start=1):
        if isinstance(week_data, dict):
            week_number = _safe_int(
                week_data.get("week", week_data.get("week_number", idx)),
                idx,
            )
            focus = week_data.get("focus") or week_data.get("title") or f"Week {week_number}"
        else:
            week_number = idx
            focus = f"Week {week_number}"

        raw_days = _extract_days_from_week(week_data)
        normalized_days = [_normalize_day(day_data, day_idx) for day_idx, day_data in enumerate(raw_days, start=1)]
        normalized_weeks.append({
            "week": week_number,
            "focus": focus,
            "days": normalized_days,
        })

    training_days = _safe_int(root.get("training_days", plan.get("training_days", 0)), 0)
    if training_days <= 0:
        training_days = max((len(week.get("days", [])) for week in normalized_weeks), default=3)

    diet = root.get("diet") if isinstance(root.get("diet"), dict) else {}
    if not diet and isinstance(plan.get("diet"), dict):
        diet = plan.get("diet")

    tips = root.get("tips") if isinstance(root.get("tips"), list) else []
    if not tips and isinstance(plan.get("tips"), list):
        tips = plan.get("tips")

    normalized_plan = dict(root)
    normalized_plan["weeks"] = normalized_weeks
    normalized_plan["training_days"] = training_days
    normalized_plan["diet"] = diet
    normalized_plan["tips"] = tips
    return normalized_plan

def get_rpe_color(rpe_str):
    try:
        rpe = float(str(rpe_str))
        if rpe <= 6:   return "#22c55e"
        elif rpe <= 7: return "#84cc16"
        elif rpe <= 8: return "#FFD700"
        elif rpe <= 9: return "#f97316"
        else:          return "#ef4444"
    except (ValueError, TypeError):
        return "#FFD700"

def show_exercise(ex):
    """Display exercise with safe field access"""
    ex = _normalize_exercise(ex)
    # Safe field extraction
    name = ex.get('name', 'Exercise')
    sets = ex.get('sets', '?')
    reps = ex.get('reps', '?')
    weight = ex.get('weight', '?')
    rpe = ex.get('rpe', '?')
    note = ex.get('note', '')
    
    c1, c2 = st.columns([9, 1])
    with c1:
        weight_str = f"{weight}kg" if weight != '?' else 'BW'
        rpe_color = get_rpe_color(rpe)
        st.markdown(f"""
        <div class="ex-card">
            <div class="ex-name">
                {name}
                <span class="ex-weight-tag">⚖️ {weight_str}</span>
            </div>
            <div class="ex-meta">
                📊 {sets} sets &nbsp;·&nbsp; 🔁 {reps} reps &nbsp;·&nbsp;
                <span style="color:{rpe_color};font-weight:600;">RPE {rpe}</span>
            </div>
            <div class="ex-note">💡 {note if note else 'Training exercise'}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        relevant = [t for t in GLOSSARY if t in f"{name} {note} rpe sets reps".lower()]
        if relevant:
            with st.popover("📖"):
                st.markdown("**Quick Glossary**")
                for term in relevant:
                    st.markdown(f"**{term.upper()}** — {GLOSSARY[term]}")

def show_dashboard(user, plan_row, log):
    from datetime import datetime
    user_id        = user.id
    plan           = _normalize_plan(plan_row.get("plan_data"))

    start_date_raw = plan_row.get("start_date")
    if not start_date_raw and isinstance(plan, dict):
        start_date_raw = plan.get("start_date")
    try:
        start_date = datetime.strptime(str(start_date_raw), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        start_date = date.today()

    today          = date.today()
    days_elapsed   = (today - start_date).days
    training_days  = plan.get("training_days", 3)

    all_sessions   = build_session_schedule(plan, start_date)
    today_session  = get_today_session(all_sessions, log)
    total_completed, total_sessions, overall_progress, total_score = calculate_progress(all_sessions, log)

    current_week   = today_session["week"] if today_session else 4
    week_sessions  = [s for s in all_sessions if s["week"] == current_week]
    week_completed = len([s for s in week_sessions if log.get(s["session_id"], {}).get("completed")])
    week_progress  = int((week_completed / len(week_sessions)) * 100) if week_sessions else 0

    # ── Program Complete ──
    if total_sessions > 0 and total_completed >= total_sessions:
        st.balloons()
        st.success("🏆 YOU COMPLETED YOUR 4-WEEK PROGRAM! ABSOLUTE BEAST MODE!")
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Sessions Done",   f"{total_completed}/{total_sessions}")
        col2.metric("🏆 Final Score",     f"{total_score} pts")
        col3.metric("📅 Days of Grinding", str(days_elapsed))
        st.divider()
        if st.button("🚀 Generate New Plan", use_container_width=True):
            archive_plan(user_id, plan, log)
            delete_plan(user_id)
            st.rerun()
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Dashboard", "📋 Full Program", "🍽️ Diet Plan", "💡 Tips", "📈 Progress"])

    # ── Tab 1: Dashboard ──
    with tab1:
        st.subheader("📊 Your Progress")
        if total_sessions == 0:
            st.warning("No calendar sessions could be derived from this saved format yet. Your plan details are still available in Full Program.")

        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Sessions Done", f"{total_completed}/{total_sessions}")
        col2.metric("🏆 Total Score",   f"{total_score} pts")
        col3.metric("📅 Day",           f"{min(days_elapsed + 1, 28)}/28")

        st.markdown("**Overall Program Progress**")
        st.progress(overall_progress / 100, text=f"{overall_progress}% Complete")
        st.markdown(f"**Week {current_week} Progress**")
        st.progress(week_progress / 100, text=f"Week {current_week}: {week_completed}/{len(week_sessions)} sessions done")
        st.divider()

        with st.expander("⚙️ Plan Options"):
            st.warning("This will delete your current plan but keep all your progress history.")
            if st.button("🔄 Generate New Plan", use_container_width=True):
                archive_plan(user_id, plan, log)
                delete_plan(user_id)
                st.rerun()

        st.divider()
        st.subheader("💪 Today's Workout")

        if today_session:
            session_id    = today_session["session_id"]
            already_logged = log.get(session_id, {}).get("completed", False)

            if already_logged:
                prev = log[session_id]
                st.success(f"✅ Already completed! Score: **{prev['score']}/100**")
                if prev.get("notes"):
                    st.caption(f"📝 {prev['notes']}")
            else:
                st.markdown(f"**{today_session['label']}** — *{today_session['week_focus']}*")
                for ex in today_session["exercises"]:
                    show_exercise(ex)

                st.divider()
                st.markdown("### 📝 Log This Session")

                with st.form(f"log_{today.strftime('%Y%m%d')}"):
                    completed     = st.checkbox("✅ I completed this workout!")
                    exercise_names = [ex["name"].lower() for ex in today_session["exercises"]]
                    has_squat     = any("squat" in e for e in exercise_names)
                    has_bench     = any("bench" in e for e in exercise_names)
                    has_deadlift  = any("deadlift" in e or "rdl" in e for e in exercise_names)

                    active_lifts = []
                    if has_squat:    active_lifts.append("squat")
                    if has_bench:    active_lifts.append("bench")
                    if has_deadlift: active_lifts.append("deadlift")

                    w_squat, w_bench, w_deadlift = 0, 0, 0
                    if active_lifts:
                        for lift in active_lifts:
                            if lift == "squat":
                                w_squat    = st.number_input("🦵 Squat kg",    min_value=0, key="log_squat")
                            elif lift == "bench":
                                w_bench    = st.number_input("💪 Bench kg",    min_value=0, key="log_bench")
                            elif lift == "deadlift":
                                w_deadlift = st.number_input("⚡ Deadlift kg", min_value=0, key="log_dead")

                    rpe_felt      = st.slider("😤 How hard did it feel? (RPE)", 1, 10, 7)
                    notes         = st.text_input("📝 Notes (optional)")
                    log_submitted = st.form_submit_button("💾 Save Session", use_container_width=True)

                if log_submitted:
                    weights_entered = (w_squat + w_bench + w_deadlift) > 0
                    score = calculate_score(completed, rpe_felt, weights_entered)
                    entry = {
                        "completed": completed,
                        "squat":     w_squat,
                        "bench":     w_bench,
                        "deadlift":  w_deadlift,
                        "rpe":       rpe_felt,
                        "notes":     notes,
                        "score":     score,
                        "date":      str(today)
                    }
                    save_log_entry(user_id, session_id, entry)
                    st.success(f"🔥 Session logged! Score: **{score}/100**")
                    st.rerun()
        else:
            if total_sessions == 0:
                st.info("Open the Full Program tab to review your exercises. Session dates will appear when schedule fields are detected.")
            else:
                st.info("🛌 Rest day today! Recovery is part of the program.")

        st.divider()
        st.subheader("📅 Full Schedule")
        if not all_sessions:
            st.info("No dated schedule generated for this plan format yet.")
        else:
            for s in all_sessions:
                sid          = s["session_id"]
                s_log        = log.get(sid, {})
                is_completed = s_log.get("completed", False)
                is_today     = s["date"] == str(today)
                is_missed    = s["date"] < str(today) and not is_completed
                score        = s_log.get("score", 0)

                if is_today:
                    icon, extra_class = "👉", "today"
                elif is_completed:
                    icon, extra_class = "✅", "completed"
                elif is_missed:
                    icon, extra_class = "❌", "missed"
                else:
                    icon, extra_class = "⬜", ""

                score_badge = f'<span style="color:#FFD700;font-size:0.8rem;margin-left:auto;">⭐ {score}/100</span>' if is_completed else ""
                st.markdown(f"""
                <div class="schedule-item {extra_class}">
                    <span style="font-size:1.1rem">{icon}</span>
                    <span style="flex:1;font-size:0.88rem;color:#bbb;">
                        <strong style="color:#e0e0e0;">Wk {s['week']}</strong> — {s['label']}
                        <span style="color:#444;font-size:0.75rem;margin-left:6px;">({s['date']})</span>
                    </span>
                    {score_badge}
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: Full Program ──
    with tab2:
        st.subheader("📋 Your Full 4-Week Program")
        weeks = plan.get("weeks", []) if isinstance(plan, dict) else []

        if not weeks:
            st.warning("No program weeks found in your saved plan. Generate a new plan to populate this section.")
            with st.expander("Show detected plan keys"):
                if isinstance(plan, dict):
                    st.write(sorted(list(plan.keys())))
                else:
                    st.write("Saved plan format is invalid")
        else:
            for week in weeks:
                st.subheader(f"Week {week.get('week', '?')} — {week.get('focus', '?')}")
                days_list = week.get("days", [])
                
                for day in days_list:
                    with st.expander(f"📅 {day.get('label', 'Day')}"):
                        exercises = day.get("exercises", [])
                        
                        if not exercises:
                            st.info("No exercises for this day")
                        else:
                            for ex in exercises:
                                show_exercise(ex)
                st.divider()

    # ── Tab 3: Diet Plan ──
    # ── Tab 3: Diet Plan ──
    with tab3:
        diet = plan.get("diet", {})
        meal_alts = diet.get("meal_alternatives", {})
        
        st.subheader("🍽️ Your Daily Diet Plan")
        
        # Show macro targets
        d_r1c1, d_r1c2 = st.columns(2)
        d_r2c1, d_r2c2 = st.columns(2)
        d_r1c1.metric("🔥 Calories", f"{diet.get('calories', 0)} kcal")
        d_r1c2.metric("🥩 Protein",  f"{diet.get('protein', 0)}g")
        d_r2c1.metric("🍚 Carbs",    f"{diet.get('carbs', 0)}g")
        d_r2c2.metric("🥑 Fats",     f"{diet.get('fats', 0)}g")
        
        # Show maintenance and TDEE
        if diet.get('maintenance'):
            st.caption(f"📊 Maintenance: {diet.get('maintenance')} kcal | TDEE: {diet.get('tdee')} kcal")
        
        st.divider()
        
        # Display meals with alternatives
        meals = diet.get("meals", [])
        for meal in meals:
            time = meal.get('time', '?')
            name = meal.get('name', '?')
            
            with st.expander(f"🕐 {time} — {name}", expanded=False):
                # Main meal
                st.markdown(f"### {meal.get('food', 'N/A')}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Protein", f"{meal.get('protein', 0)}g")
                c2.metric("Carbs",   f"{meal.get('carbs', 0)}g")
                c3.metric("Fats",    f"{meal.get('fats', 0)}g")
                
                # Show alternatives
                if meal_alts:
                    st.markdown("---")
                    st.markdown("**🔄 Alternative Options:**")
                    
                    # Find matching time slot in alternatives
                    for alt_time, alt_options in meal_alts.items():
                        if time in alt_time:
                            for i, alt in enumerate(alt_options, 1):
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"**Option {i}:** {alt['food']}")
                                with col2:
                                    st.caption(f"P:{alt['protein']}g | C:{alt['carbs']}g | F:{alt['fats']}g")
                            break

    # ── Tab 4: Tips ──
    with tab4:
        st.subheader("💡 Coach's Tips")
        tips = plan.get("tips", [])
        
        for i, tip in enumerate(tips, 1):
            st.info(f"💡 **Tip {i}:** {tip}")

    # ── Tab 5: Progress Dashboard ──
    with tab5:
        st.markdown("""
        <div class="progress-header">
            <div class="progress-title">📈 STRENGTH JOURNEY</div>
            <div class="progress-sub">Your performance data — session by session</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Build DataFrame from log ──
        progress_rows = []
        for sid, entry in log.items():
            if entry.get("completed") and entry.get("date"):
                progress_rows.append({
                    "Session":     sid,
                    "Date":        entry.get("date", ""),
                    "Squat":       float(entry.get("squat",    0) or 0),
                    "Bench":       float(entry.get("bench",    0) or 0),
                    "Deadlift":    float(entry.get("deadlift", 0) or 0),
                    "RPE":         float(entry.get("rpe",      7) or 7),
                    "Score":       int(entry.get("score",      0) or 0),
                    "Notes":       entry.get("notes", "") or "",
                })

        if not progress_rows:
            st.markdown("""
            <div class="empty-progress">
                <span class="empty-icon">🏋️</span>
                <h3>No Progress Data Yet</h3>
                <p>Complete your first workout and log your weights.<br>
                Your strength journey starts here — come back after your first session!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            df = (
                pd.DataFrame(progress_rows)
                .sort_values("Date")
                .reset_index(drop=True)
            )

            # ── PR Summary Cards ──
            def safe_max(series):
                s = series[series > 0]
                return s.max() if not s.empty else 0.0

            def delta_html(val):
                if val > 0:   return f'<span class="lift-pr-delta positive">▲ +{val:.0f} kg</span>'
                elif val < 0: return f'<span class="lift-pr-delta negative">▼ {val:.0f} kg</span>'
                else:         return f'<span class="lift-pr-delta neutral">— no change</span>'

            def lift_delta(series):
                """Delta between first and last session where this lift was logged (>0)."""
                s = series[series > 0]
                if len(s) < 2:
                    return 0.0
                return float(s.iloc[-1] - s.iloc[0])

            sq_max  = safe_max(df["Squat"])
            bp_max  = safe_max(df["Bench"])
            dl_max  = safe_max(df["Deadlift"])
            sq_d    = lift_delta(df["Squat"])
            bp_d    = lift_delta(df["Bench"])
            dl_d    = lift_delta(df["Deadlift"])
            total_s = int(df["Score"].sum())

            c1, c2, c3, c4 = st.columns(4)
            cards = [
                (c1, "🦵", "SQUAT PR",    sq_max,  sq_d),
                (c2, "💪", "BENCH PR",    bp_max,  bp_d),
                (c3, "⚡", "DEADLIFT PR", dl_max,  dl_d),
            ]
            for col, icon, label, val, delta in cards:
                with col:
                    val_str = f"{val:.0f} kg" if val > 0 else "—"
                    st.markdown(f"""
                    <div class="lift-pr-card">
                        <span class="lift-pr-icon">{icon}</span>
                        <div class="lift-pr-label">{label}</div>
                        <div class="lift-pr-value">{val_str}</div>
                        {delta_html(delta) if val > 0 else ''}
                    </div>
                    """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="lift-pr-card">
                    <span class="lift-pr-icon">🏆</span>
                    <div class="lift-pr-label">TOTAL SCORE</div>
                    <div class="lift-pr-value">{total_s}</div>
                    <span class="lift-pr-delta neutral">{len(df)} sessions logged</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Strength Progression Chart ──
            lift_df = df[["Date", "Squat", "Bench", "Deadlift"]].copy()
            has_lifts = (lift_df["Squat"] > 0).any() or (lift_df["Bench"] > 0).any() or (lift_df["Deadlift"] > 0).any()

            st.markdown('<div class="chart-section"><div class="chart-title">💹 Strength Progression</div>', unsafe_allow_html=True)
            if has_lifts:
                chart_df = lift_df.set_index("Date")
                chart_df = chart_df[(chart_df > 0).any(axis=1)]
                chart_df = chart_df.replace(0, float("nan"))
                st.line_chart(
                    chart_df,
                    color=["#FFD700", "#F97316", "#EF4444"],
                    height=280,
                    use_container_width=True,
                )
                st.caption("🟡 Squat  🟠 Bench  🔴 Deadlift  (kg logged per session)")
            else:
                st.info("Log weight values when completing sessions to see your strength progression chart.")
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Score & RPE Charts (side by side) ──
            ch1, ch2 = st.columns(2)

            with ch1:
                st.markdown('<div class="chart-section"><div class="chart-title">⭐ Session Scores</div>', unsafe_allow_html=True)
                score_df = df[["Date", "Score"]].set_index("Date")
                st.bar_chart(score_df, color="#FFD700", height=220, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with ch2:
                st.markdown('<div class="chart-section"><div class="chart-title">😤 Training Intensity (RPE)</div>', unsafe_allow_html=True)
                rpe_df = df[["Date", "RPE"]].set_index("Date")
                st.area_chart(rpe_df, color="#F97316", height=220, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Session History Table ──
            st.divider()
            st.markdown("### 📊 Full Session Log")

            st.markdown("""
            <div class="session-table-row">
                <span class="session-table-head">Date</span>
                <span class="session-table-head">🦵 Squat</span>
                <span class="session-table-head">💪 Bench</span>
                <span class="session-table-head">⚡ Deadlift</span>
                <span class="session-table-head">RPE</span>
                <span class="session-table-head">Score</span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in df.iterrows():
                sq_str  = f"{row['Squat']:.0f} kg"    if row["Squat"]    > 0 else "—"
                bp_str  = f"{row['Bench']:.0f} kg"    if row["Bench"]    > 0 else "—"
                dl_str  = f"{row['Deadlift']:.0f} kg" if row["Deadlift"] > 0 else "—"
                score_color = "#22c55e" if row["Score"] >= 80 else ("#FFD700" if row["Score"] >= 50 else "#ef4444")
                st.markdown(f"""
                <div class="session-table-row">
                    <span style="color:#bbb">{row['Date']}</span>
                    <span style="color:#FFD700;font-weight:600">{sq_str}</span>
                    <span style="color:#F97316;font-weight:600">{bp_str}</span>
                    <span style="color:#EF4444;font-weight:600">{dl_str}</span>
                    <span style="color:#999">{row['RPE']:.0f}</span>
                    <span style="color:{score_color};font-weight:700">{row['Score']}</span>
                </div>
                """, unsafe_allow_html=True)

            if df[df["Notes"] != ""].shape[0] > 0:
                st.divider()
                st.markdown("### 📝 Session Notes")
                for _, row in df[df["Notes"] != ""].iterrows():
                    st.markdown(f"""
                    <div class="ex-card" style="border-left-color:#F97316">
                        <div class="ex-note" style="font-style:normal;color:#aaa">
                            <strong style="color:#F97316">{row['Date']}</strong> — {row['Notes']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)