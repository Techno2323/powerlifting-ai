import streamlit as st
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
    except:
        return "#FFD700"

def show_exercise(ex):
    c1, c2 = st.columns([11, 1])
    with c1:
        weight_str = ex.get('weight', 'Bodyweight')
        rpe_val    = ex.get('rpe', '?')
        rpe_color  = get_rpe_color(rpe_val)
        st.markdown(f"""
        <div class="ex-card">
            <div class="ex-name">
                {ex['name']}
                <span class="ex-weight-tag">⚖️ {weight_str}</span>
            </div>
            <div class="ex-meta">
                📊 {ex['sets']} sets &nbsp;·&nbsp; 🔁 {ex['reps']} reps &nbsp;·&nbsp;
                <span style="color:{rpe_color};font-weight:600;">RPE {rpe_val}</span>
            </div>
            <div class="ex-note">💡 {ex['note']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        relevant = [t for t in GLOSSARY if t in f"{ex['name']} {ex['note']} rpe sets reps".lower()]
        if relevant:
            with st.popover("📖"):
                st.markdown("**Quick Glossary**")
                for term in relevant:
                    st.markdown(f"**{term.upper()}** — {GLOSSARY[term]}")

def show_dashboard(user, plan_row, log):
    from datetime import datetime
    user_id        = user.id
    plan           = plan_row["plan_data"]
    start_date     = datetime.strptime(plan_row["start_date"], "%Y-%m-%d").date()
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
    if total_completed >= total_sessions:
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

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📋 Full Program", "🍽️ Diet Plan", "💡 Tips"])

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
                    completed = st.checkbox("✅ I completed this workout!")
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
                        lift_cols = st.columns(len(active_lifts))
                        for i, lift in enumerate(active_lifts):
                            with lift_cols[i]:
                                if lift == "squat":
                                    w_squat    = st.number_input("🦵 Squat (kg)",    min_value=0)
                                elif lift == "bench":
                                    w_bench    = st.number_input("💪 Bench (kg)",    min_value=0)
                                elif lift == "deadlift":
                                    w_deadlift = st.number_input("⚡ Deadlift (kg)", min_value=0)

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
        for week in plan["weeks"]:
            st.subheader(f"Week {week['week']} — {week['focus']}")
            for day in week["days"]:
                with st.expander(f"📅 {day['label']}"):
                    for ex in day["exercises"]:
                        weight_str = ex.get('weight', 'BW')
                        st.markdown(f"""
                        <div class="ex-card">
                            <div class="ex-name">{ex['name']} <span class="ex-weight-tag">⚖️ {weight_str}</span></div>
                            <div class="ex-meta">📊 {ex['sets']} × {ex['reps']} · <span style="color:{get_rpe_color(ex.get('rpe','7'))};font-weight:600;">RPE {ex.get('rpe','?')}</span></div>
                            <div class="ex-note">💡 {ex['note']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.divider()

    # ── Tab 3: Diet Plan ──
    with tab3:
        diet = plan["diet"]
        st.subheader("🍽️ Your Daily Indian Diet Plan")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🔥 Calories", f"{diet['calories']} kcal")
        m2.metric("🥩 Protein",  f"{diet['protein']}g")
        m3.metric("🍚 Carbs",    f"{diet['carbs']}g")
        m4.metric("🥑 Fats",     f"{diet['fats']}g")
        st.divider()
        for meal in diet["meals"]:
            with st.expander(f"🕐 {meal['time']} — {meal['name']}"):
                st.markdown(f"**{meal['food']}**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Protein", f"{meal['protein']}g")
                c2.metric("Carbs",   f"{meal['carbs']}g")
                c3.metric("Fats",    f"{meal['fats']}g")

    # ── Tab 4: Tips ──
    with tab4:
        st.subheader("💡 Coach's Tips")
        for i, tip in enumerate(plan["tips"], 1):
            st.info(f"💡 **Tip {i}:** {tip}")