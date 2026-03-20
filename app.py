import google.generativeai as genai
import streamlit as st
import json
import os
from datetime import date, datetime, timedelta
import pandas as pd

genai.configure(api_key="AIzaSyCxqJ0jLDo_bMhZl8FUvVmdN4X1-wsyF6c")
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Indian Powerlifting AI Coach", page_icon="🏋️", layout="wide")

# ---- File Helpers ----
PLAN_FILE = "saved_plan.json"
LOG_FILE = "workout_log.json"
HISTORY_FILE = "workout_history.json"

def load_plan():
    if os.path.exists(PLAN_FILE):
        with open(PLAN_FILE, "r") as f:
            return json.load(f)
    return None

def save_plan(plan):
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f, indent=2)

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def calculate_score(completed, rpe, weights_entered):
    score = 0
    if completed:
        score += 50  # Base score for showing up
    if rpe > 0:
        # RPE 7-10, higher effort = higher score (max 30 pts)
        score += min(int((rpe / 10) * 30), 30)
    if weights_entered:
        score += 20  # Bonus for logging weights
    return score

def archive_log(log, plan):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    history.append({
        "plan_start": plan.get("start_date"),
        "plan_goal": plan.get("goal"),
        "log": log
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ---- Main App ----
st.title("🏋️ Indian Powerlifting AI Coach")
st.caption("Built for Indian athletes. Real food. Real strength.")

plan = load_plan()
log = load_log()

# ================================================
# NO PLAN YET — Show Generator
# ================================================
if plan is None:
    st.info("👋 No active plan found. Generate your first plan below!")
    
    with st.form("user_form"):
        col1, col2 = st.columns(2)
        with col1:
            squat = st.number_input("🦵 Best Squat (kg)", min_value=0)
            bench = st.number_input("💪 Best Bench Press (kg)", min_value=0)
            deadlift = st.number_input("⚡ Best Deadlift (kg)", min_value=0)
        with col2:
            goal = st.selectbox("🎯 Your Goal", ["Build Strength", "Bulk", "Cut"])
            days = st.selectbox("📅 Training Days/Week", [3, 4, 5, 6])
            food = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])
        
        submitted = st.form_submit_button("🚀 Generate My Plan", use_container_width=True)

    if submitted:
        prompt = f"""
        You are an expert powerlifting coach for Indian athletes.
        User stats:
        - Squat: {squat} kg, Bench: {bench} kg, Deadlift: {deadlift} kg
        - Goal: {goal}, Training days per week: {days}, Diet: {food}

        Return ONLY valid JSON, no markdown, no backticks, no extra text.
        {{
            "summary": "2 line motivational summary",
            "goal": "{goal}",
            "weeks": [
                {{
                    "week": 1,
                    "focus": "one line focus",
                    "days": [
                        {{
                            "day_number": 1,
                            "label": "Day 1 - Squat Emphasis",
                            "exercises": [
                                {{"name": "Squat", "sets": 3, "reps": "6", "rpe": "7", "note": "focus on depth"}}
                            ]
                        }}
                    ]
                }}
            ],
            "diet": {{
                "calories": 3000,
                "protein": 160,
                "carbs": 420,
                "fats": 75,
                "meals": [
                    {{
                        "time": "8:00 AM",
                        "name": "Breakfast",
                        "food": "Paneer bhurji with 2 rotis",
                        "protein": 35,
                        "carbs": 60,
                        "fats": 20
                    }}
                ]
            }},
            "tips": ["tip 1", "tip 2", "tip 3"]
        }}
        Generate all 4 weeks with {days} training days each.
        """
        with st.spinner("Building your personalized plan... 🔥"):
            try:
                response = model.generate_content(prompt)
                raw = response.text.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                data = json.loads(raw)
                data["start_date"] = str(date.today())
                data["training_days"] = days
                save_plan(data)
                st.success("✅ Plan generated and saved! Refresh the page to start tracking.")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# ================================================
# PLAN EXISTS — Show Dashboard
# ================================================
else:
    start_date = datetime.strptime(plan["start_date"], "%Y-%m-%d").date()
    today = date.today()
    days_elapsed = (today - start_date).days
    training_days = plan["training_days"]
    total_sessions = training_days * 4  # 4 weeks

    # Build flat list of all sessions with their real dates
    # Assign training days evenly (skip rest days)
    all_sessions = []
    session_index = 0
    current_date = start_date
    for week in plan["weeks"]:
        for day in week["days"]:
            all_sessions.append({
                "session_id": f"w{week['week']}_d{day['day_number']}",
                "week": week["week"],
                "week_focus": week["focus"],
                "label": day["label"],
                "exercises": day["exercises"],
                "date": str(current_date)
            })
            # Space out sessions with rest days
            gap = 7 // training_days
            current_date += timedelta(days=gap)

    # Figure out today's session
    today_session = None
    for s in all_sessions:
        if s["date"] == str(today):
            today_session = s
            break
    # If no exact match, find closest upcoming
    if today_session is None:
        for s in all_sessions:
            if s["date"] >= str(today) and s["session_id"] not in log:
                today_session = s
                break

    # ---- Progress Calculation ----
    completed_sessions = [s for s in all_sessions if log.get(s["session_id"], {}).get("completed")]
    total_completed = len(completed_sessions)
    overall_progress = int((total_completed / total_sessions) * 100)

    # Current week sessions
    if today_session:
        current_week = today_session["week"]
    else:
        current_week = 4
    week_sessions = [s for s in all_sessions if s["week"] == current_week]
    week_completed = len([s for s in week_sessions if log.get(s["session_id"], {}).get("completed")])
    week_progress = int((week_completed / len(week_sessions)) * 100) if week_sessions else 0

    # Total score
    total_score = sum(log.get(s["session_id"], {}).get("score", 0) for s in all_sessions)
    max_score = total_sessions * 100

    # ---- Check if Program Complete ----
    program_complete = total_completed >= total_sessions

    if program_complete:
        st.balloons()
        st.success("🏆 YOU COMPLETED YOUR 4-WEEK PROGRAM! ABSOLUTE BEAST MODE!")
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Sessions Done", f"{total_completed}/{total_sessions}")
        col2.metric("🏆 Final Score", f"{total_score}/{max_score}")
        col3.metric("📅 Days of Grinding", str(days_elapsed))
        
        st.divider()
        st.markdown("### Ready for your next program?")
        if st.button("🚀 Generate New Plan", use_container_width=True):
            archive_log(log, plan)
            os.remove(PLAN_FILE)
            os.remove(LOG_FILE)
            st.rerun()
    else:
        # ---- Navigation Tabs ----
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📋 Full Program", "🍽️ Diet Plan", "💡 Tips"])

        # ================================================
        # TAB 1 — DASHBOARD
        # ================================================
        with tab1:
            # Progress Section
            st.subheader("📊 Your Progress")
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Sessions Done", f"{total_completed}/{total_sessions}")
            col2.metric("🏆 Total Score", f"{total_score} pts")
            col3.metric("📅 Day", f"{min(days_elapsed + 1, 28)}/28")

            st.markdown("**Overall Program Progress**")
            st.progress(overall_progress / 100, text=f"{overall_progress}% Complete")
            
            st.markdown(f"**Week {current_week} Progress**")
            st.progress(week_progress / 100, text=f"Week {current_week}: {week_completed}/{len(week_sessions)} sessions done")

            st.divider()


            # Reset Plan Button
            with st.expander("⚙️ Plan Options"):
                st.warning("This will delete your current plan but keep all your progress history.")
                if st.button("🔄 Generate New Plan", use_container_width=True):
                    archive_log(log, plan)
                    os.remove(PLAN_FILE)
                    os.remove(LOG_FILE)
                    st.rerun()

            st.divider()

            # Today's Workout
            st.subheader("💪 Today's Workout")
            
            if today_session:
                session_id = today_session["session_id"]
                already_logged = log.get(session_id, {}).get("completed", False)

                if already_logged:
                    prev = log[session_id]
                    st.success(f"✅ Already completed! Score: **{prev['score']}/100**")
                    if prev.get("notes"):
                        st.caption(f"📝 Notes: {prev['notes']}")
                else:
                    st.markdown(f"**{today_session['label']}** — *{today_session['week_focus']}*")
                    
                    # Show exercises
                   # Glossary of terms
                    glossary = {
                        "rpe": "RPE = Rate of Perceived Exertion. A scale from 1-10 that tells you how hard to push. RPE 7 = you could do 3 more reps. RPE 8 = 2 more reps. RPE 9 = 1 more rep. RPE 10 = absolute max.",
                        "sets": "Sets = how many times you repeat a group of reps. Example: 3 sets means you do the exercise 3 times with rest in between.",
                        "reps": "Reps = Repetitions. How many times you lift in one set. Example: 6 reps means lift 6 times in a row.",
                        "rdl": "RDL = Romanian Deadlift. A deadlift variation where you hinge at the hips with a slight knee bend. Great for hamstrings and lower back.",
                        "ohp": "OHP = Overhead Press. You press a barbell from your shoulders straight above your head. Builds shoulders and triceps.",
                        "amrap": "AMRAP = As Many Reps As Possible. Do as many reps as you can with good form in that set.",
                        "deload": "Deload = A lighter week where you reduce weight and volume. Helps your body recover and come back stronger.",
                        }

                    def show_exercise(ex):
                        col1, col2 = st.columns([6, 1])
                        with col1:
                             st.markdown(f"> **{ex['name']}** — {ex['sets']} sets × {ex['reps']} reps @ RPE {ex['rpe']}  \n> *{ex['note']}*")
                        with col2:
                             # Detect which glossary terms are relevant to this exercise
                            relevant = []
                            text = f"{ex['name']} {ex['note']} rpe sets reps".lower()
                            for term in glossary:
                                if term in text:
                                    relevant.append(term)
                                
                            if relevant:
                                with st.popover("💡"):
                                    st.markdown("**📖 Quick Glossary**")
                                    for term in relevant:
                                        st.markdown(f"**{term.upper()}** — {glossary[term]}")

                    for ex in today_session["exercises"]:
                        show_exercise(ex)
                                            
                    st.divider()
                    st.markdown("### 📝 Log This Session")

                    with st.form("session_log_form"):
                        completed = st.checkbox("✅ I completed this workout!", value=False)
                        
                        st.markdown("**How much did you lift? (your top set)**")
                        # Detect which main lifts are in today's session
                        exercise_names = [ex["name"].lower() for ex in today_session["exercises"]]
                        has_squat = any("squat" in e for e in exercise_names)
                        has_bench = any("bench" in e for e in exercise_names)
                        has_deadlift = any("deadlift" in e or "rdl" in e for e in exercise_names)

                        # Only show inputs for lifts in today's workout
                        active_lifts = []
                        if has_squat: active_lifts.append("squat")
                        if has_bench: active_lifts.append("bench")
                        if has_deadlift: active_lifts.append("deadlift")

                        lift_cols = st.columns(len(active_lifts)) if active_lifts else st.columns(1)

                        w_squat, w_bench, w_deadlift = 0, 0, 0

                        for i, lift in enumerate(active_lifts):
                            with lift_cols[i]:
                                if lift == "squat":
                                    w_squat = st.number_input("🦵 Squat (kg)", min_value=0)
                                elif lift == "bench":
                                    w_bench = st.number_input("💪 Bench (kg)", min_value=0)
                                elif lift == "deadlift":
                                    w_deadlift = st.number_input("⚡ Deadlift (kg)", min_value=0)

                        if not active_lifts:
                            st.info("No main lifts detected for today — just log your RPE and notes!")

                        
                        rpe_felt = st.slider("😤 How hard did it feel? (RPE)", 1, 10, 7)
                        notes = st.text_input("📝 Notes (optional)", placeholder="e.g. squats felt great today!")
                        
                        log_submitted = st.form_submit_button("💾 Save Session", use_container_width=True)

                    if log_submitted:
                        weights_entered = (w_squat + w_bench + w_deadlift) > 0
                        score = calculate_score(completed, rpe_felt, weights_entered)
                        log[session_id] = {
                            "completed": completed,
                            "squat": w_squat,
                            "bench": w_bench,
                            "deadlift": w_deadlift,
                            "rpe": rpe_felt,
                            "notes": notes,
                            "score": score,
                            "date": str(today)
                        }
                        save_log(log)
                        st.success(f"🔥 Session logged! You scored **{score}/100** today!")
                        st.rerun()
            else:
                st.info("🛌 Rest day today! Recovery is part of the program. Come back tomorrow.")

            st.divider()

            # All Sessions Overview
            st.subheader("📅 Full Schedule")
            for s in all_sessions:
                sid = s["session_id"]
                s_log = log.get(sid, {})
                is_completed = s_log.get("completed", False)
                is_today = s["date"] == str(today)
                score = s_log.get("score", 0)

                if is_today:
                    icon = "👉"
                elif is_completed:
                    icon = "✅"
                elif s["date"] < str(today):
                    icon = "❌"
                else:
                    icon = "⬜"

                label = f"{icon} **Week {s['week']} — {s['label']}** ({s['date']})"
                if is_completed:
                    label += f" — Score: {score}/100"
                st.markdown(label)

        # ================================================
        # TAB 2 — FULL PROGRAM
        # ================================================
        with tab2:
            st.subheader("📋 Your Full 4-Week Program")
            for week in plan["weeks"]:
                st.subheader(f"Week {week['week']} — {week['focus']}")
                cols = st.columns(len(week["days"]))
                for i, day in enumerate(week["days"]):
                    with cols[i]:
                        st.markdown(f"**{day['label']}**")
                        for ex in day["exercises"]:
                            st.markdown(f"> **{ex['name']}**  \n> {ex['sets']} × {ex['reps']} @ RPE {ex['rpe']}  \n> *{ex['note']}*")
                st.divider()

        # ================================================
        # TAB 3 — DIET
        # ================================================
        with tab3:
            diet = plan["diet"]
            st.subheader("🍽️ Your Daily Indian Diet Plan")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("🔥 Calories", f"{diet['calories']} kcal")
            m2.metric("🥩 Protein", f"{diet['protein']}g")
            m3.metric("🍚 Carbs", f"{diet['carbs']}g")
            m4.metric("🥑 Fats", f"{diet['fats']}g")
            st.divider()
            for meal in diet["meals"]:
                with st.expander(f"🕐 {meal['time']} — {meal['name']}"):
                    st.write(f"**{meal['food']}**")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Protein", f"{meal['protein']}g")
                    c2.metric("Carbs", f"{meal['carbs']}g")
                    c3.metric("Fats", f"{meal['fats']}g")

        # ================================================
        # TAB 4 — TIPS
        # ================================================
        with tab4:
            st.subheader("💡 Coach's Tips")
            for i, tip in enumerate(plan["tips"], 1):
                st.info(f"💡 **Tip {i}:** {tip}")