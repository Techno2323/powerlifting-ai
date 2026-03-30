import streamlit as st
import pandas as pd
import re
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


def _normalize_plan_weeks(plan):
    """Return a consistent weeks[] -> days[] -> exercises[] structure."""
    if not isinstance(plan, dict):
        return []

    candidates = [
        plan,
        plan.get("training"),
        plan.get("program"),
        plan.get("plan"),
        plan.get("training_plan"),
    ]

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        weeks = candidate.get("weeks")
        if isinstance(weeks, list) and weeks:
            normalized = []
            for idx, week in enumerate(weeks, 1):
                if not isinstance(week, dict):
                    continue

                days_list = week.get("days")
                if not isinstance(days_list, list) or not days_list:
                    # Backward compatibility: convert day1_ex/day2_ex... into days[].
                    day_keys = [k for k in week.keys() if re.match(r"^day\d+_ex$", str(k))]
                    day_keys.sort(key=lambda k: int(re.findall(r"\d+", k)[0]))
                    rebuilt_days = []
                    for d_i, day_key in enumerate(day_keys, 1):
                        ex_list = week.get(day_key, [])
                        if isinstance(ex_list, list):
                            rebuilt_days.append({
                                "day_number": d_i,
                                "label": f"Day {d_i}",
                                "exercises": ex_list,
                            })
                    days_list = rebuilt_days

                safe_days = [d for d in (days_list or []) if isinstance(d, dict)]
                normalized.append({
                    "week": week.get("week", idx),
                    "focus": week.get("focus", "Training"),
                    "days": safe_days,
                })

            if normalized:
                return normalized

        # Fallback for plans that store only top-level days.
        top_days = candidate.get("days")
        if isinstance(top_days, list) and top_days:
            return [{
                "week": 1,
                "focus": candidate.get("focus", "Training Program"),
                "days": [d for d in top_days if isinstance(d, dict)],
            }]

    return []

def show_dashboard(user, plan_row, log):
    from datetime import datetime
    user_id        = user.id
    plan           = plan_row["plan_data"]

    normalized_weeks = _normalize_plan_weeks(plan)
    schedule_plan = dict(plan) if isinstance(plan, dict) else {}
    schedule_plan["weeks"] = normalized_weeks

    if not schedule_plan.get("training_days"):
        first_week_days = len(normalized_weeks[0].get("days", [])) if normalized_weeks else 3
        schedule_plan["training_days"] = max(1, first_week_days)

    start_date     = datetime.strptime(plan_row["start_date"], "%Y-%m-%d").date()
    today          = date.today()
    days_elapsed   = (today - start_date).days
    training_days  = schedule_plan.get("training_days", 3)

    all_sessions   = build_session_schedule(schedule_plan, start_date)
    today_session  = get_today_session(all_sessions, log)
    total_completed, total_sessions, overall_progress, total_score = calculate_progress(all_sessions, log)

    # ── Guard: empty schedule means plan data is malformed ──
    if total_sessions == 0:
        st.error("⚠️ No training sessions found in your current plan. The plan data may be incomplete.")
        if st.button("🔄 Regenerate Plan", use_container_width=True):
            archive_plan(user_id, plan, log)
            delete_plan(user_id)
            st.rerun()
        return

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
            st.info("🛌 Rest day today! Recovery is part of the program.")

        st.divider()
        st.subheader("📅 Full Schedule")
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
        weeks = normalized_weeks

        if not weeks:
            st.warning("No program weeks found in your saved plan. Generate a new plan to populate this section.")
            with st.expander("Show detected plan keys"):
                if isinstance(plan, dict):
                    st.write(sorted(list(plan.keys())))
                else:
                    st.write("Saved plan format is invalid")
        else:
            for week in weeks:
                week_num = week.get("week", "?")
                st.subheader(f"Week {week_num} — {week.get('focus', '?')}")
                days_list = week.get("days", [])

                if not days_list:
                    st.info(f"No day structure found for Week {week_num}.")

                for day_i, day in enumerate(days_list, 1):
                    day_num = day.get("day_number", day_i)
                    day_label = day.get("label", f"Day {day_num}")
                    with st.expander(f"📅 Week {week_num} · Day {day_num} — {day_label}"):
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