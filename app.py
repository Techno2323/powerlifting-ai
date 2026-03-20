import google.generativeai as genai
import streamlit as st
import json
import os
from datetime import date, datetime, timedelta
import pandas as pd
from supabase import create_client

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0a0a0a;
        color: #e0e0e0;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #111111 50%, #0d0d0d 100%);
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* Title */
    h1 {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: center;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Subheaders */
    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }

    /* Hero Box */
    .hero-box {
        background: linear-gradient(135deg, #1a1a1a, #111);
        border: 1px solid #FFD70033;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 40px #FFD70011;
        animation: fadeInUp 0.8s ease;
    }

    .hero-box h2 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #FFD700 !important;
        font-size: 2rem !important;
        margin-bottom: 10px;
    }

    .hero-box p {
        color: #aaa;
        font-size: 1rem;
        line-height: 1.8;
    }

    /* Hero Stats */
    .hero-stat {
        display: inline-block;
        background: #FFD70011;
        border: 1px solid #FFD70033;
        border-radius: 12px;
        padding: 15px 25px;
        margin: 8px;
        text-align: center;
        animation: fadeInUp 1s ease;
    }

    .hero-stat .number {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2rem;
        color: #FFD700;
        font-weight: 700;
    }

    .hero-stat .label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px #FFD70033 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px #FFD70055 !important;
    }

    /* Input fields */
    .stTextInput input {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #fff !important;
        padding: 12px !important;
        transition: border 0.3s ease;
    }

    .stTextInput input:focus {
        border: 1px solid #FFD700 !important;
        box-shadow: 0 0 10px #FFD70033 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #111;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #222;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: #1a1a1a;
        border: 1px solid #FFD70022;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px #00000055;
    }

    [data-testid="metric-container"]:hover {
        border-color: #FFD700;
        box-shadow: 0 0 20px #FFD70033;
        transform: translateY(-3px);
    }

    [data-testid="metric-container"] label {
        color: #888 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 10px #FFD70066 !important;
        animation: glowPulse 2s infinite;
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 10px #FFD70066; }
        50% { box-shadow: 0 0 20px #FFD700aa; }
    }

    /* Exercise cards */
    blockquote {
        background: #1a1a1a !important;
        border-left: 3px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px #00000044 !important;
    }

    blockquote:hover {
        background: #222 !important;
        box-shadow: 0 4px 20px #FFD70022 !important;
        transform: translateX(5px) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        color: #FFD700 !important;
        font-weight: 600 !important;
    }

    /* Success / Info boxes */
    .stSuccess {
        background: #0a1f0a !important;
        border: 1px solid #00ff0033 !important;
        border-radius: 12px !important;
    }

    .stInfo {
        background: #1a1500 !important;
        border: 1px solid #FFD70033 !important;
        border-radius: 12px !important;
    }

    /* Selectbox & number input */
    .stSelectbox > div, .stNumberInput > div {
        background: #1a1a1a !important;
        border-radius: 10px !important;
    }

    /* Divider */
    hr {
        border-color: #FFD70022 !important;
        margin: 20px 0 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #111; }
    ::-webkit-scrollbar-thumb { background: #FFD70066; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #FFD700; }
    </style>
    """, unsafe_allow_html=True)


# ---- Init ----
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.set_page_config(page_title="Indian Powerlifting AI Coach", page_icon="🏋️", layout="wide")

# ================================================
# AUTH FUNCTIONS
# ================================================
def sign_up(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)

def sign_in_google():
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "https://powerlifting-ai.streamlit.app"
            }
        })
        return res
    except Exception as e:
        return None
    
def sign_out():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()

def get_user():
    try:
        return supabase.auth.get_user()
    except:
        return None

# ================================================
# DATABASE FUNCTIONS
# ================================================
def load_plan(user_id):
    try:
        res = supabase.table("plans").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        if res.data:
            return res.data[0]
        return None
    except:
        return None

def save_plan(user_id, plan_data):
    try:
        # Delete old plan first
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        # Save new plan
        supabase.table("plans").insert({
            "user_id": user_id,
            "plan_data": plan_data,
            "start_date": plan_data["start_date"]
        }).execute()
    except Exception as e:
        st.error(f"Error saving plan: {e}")

def load_logs(user_id):
    try:
        res = supabase.table("workout_logs").select("*").eq("user_id", user_id).execute()
        # Convert to dict keyed by session_id
        return {row["session_id"]: row for row in res.data}
    except:
        return {}

def save_log_entry(user_id, session_id, entry):
    try:
        # Check if exists
        existing = supabase.table("workout_logs").select("id").eq("user_id", user_id).eq("session_id", session_id).execute()
        if existing.data:
            supabase.table("workout_logs").update(entry).eq("user_id", user_id).eq("session_id", session_id).execute()
        else:
            entry["user_id"] = user_id
            entry["session_id"] = session_id
            supabase.table("workout_logs").insert(entry).execute()
    except Exception as e:
        st.error(f"Error saving log: {e}")

def archive_plan(user_id, plan_data, log_data):
    try:
        supabase.table("plan_history").insert({
            "user_id": user_id,
            "plan_data": plan_data,
            "log_data": log_data
        }).execute()
    except Exception as e:
        st.error(f"Error archiving: {e}")

def delete_plan(user_id):
    try:
        supabase.table("plans").delete().eq("user_id", user_id).execute()
        supabase.table("workout_logs").delete().eq("user_id", user_id).execute()
    except Exception as e:
        st.error(f"Error deleting plan: {e}")

def calculate_score(completed, rpe, weights_entered):
    score = 0
    if completed:
        score += 50
    if rpe > 0:
        score += min(int((rpe / 10) * 30), 30)
    if weights_entered:
        score += 20
    return score

# ================================================
# LOGIN SCREEN
# ================================================
def show_login():
    st.title("🏋️ Indian Powerlifting AI Coach")
    st.caption("Built for Indian athletes. Real food. Real strength.")
    st.markdown("""
    <div class="hero-box">
        <h2>🏋️ FORGE YOUR STRENGTH</h2>
        <p>India's first AI powerlifting coach built for <strong style="color:#FFD700">Indian athletes</strong>.<br>
        Real food. Real programming. Real results.</p>
        <br>
        <div class="hero-stat">
            <div class="number">4</div>
            <div class="label">Week Program</div>
        </div>
        <div class="hero-stat">
            <div class="number">AI</div>
            <div class="label">Personalized</div>
        </div>
        <div class="hero-stat">
            <div class="number">🇮🇳</div>
            <div class="label">Indian Diet</div>
        </div>
        <div class="hero-stat">
            <div class="number">FREE</div>
            <div class="label">Always</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab_login:
            st.markdown("### Welcome back!")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                if email and password:
                    res, err = sign_in(email, password)
                    if err:
                        st.error(f"Login failed: {err}")
                    else:
                        st.session_state["user"] = res.user
                        st.success("Welcome back! 💪")
                        st.rerun()
                else:
                    st.warning("Please enter email and password")


        with tab_signup:
            st.markdown("### Create your account!")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

            if st.button("Create Account", use_container_width=True):
                if not new_email or not new_password:
                    st.warning("Please fill all fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    res, err = sign_up(new_email, new_password)
                    if err:
                        st.error(f"Signup failed: {err}")
                    else:
                        st.success("✅ Account created! Please check your email to verify, then login.")



# ================================================
# MAIN APP
# ================================================
def show_app(user):
    user_id = user.id

    # Top bar
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🏋️ Indian Powerlifting AI Coach")
        st.caption(f"Welcome, {user.email} 👋")
    with col2:
        if st.button("🚪 Logout"):
            sign_out()

    # Load data
    plan_row = load_plan(user_id)
    log = load_logs(user_id)

    # ================================================
    # NO PLAN — Show Generator
    # ================================================
    if plan_row is None:
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
                "training_days": {days},
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
                    save_plan(user_id, data)
                    st.success("✅ Plan generated! Refreshing...")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # ================================================
    # PLAN EXISTS — Show Dashboard
    # ================================================
    else:
        plan = plan_row["plan_data"]
        start_date = datetime.strptime(plan_row["start_date"], "%Y-%m-%d").date()
        today = date.today()
        days_elapsed = (today - start_date).days
        training_days = plan.get("training_days", 3)
        total_sessions = training_days * 4

        # Build session schedule
        all_sessions = []
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
                gap = 7 // training_days
                current_date += timedelta(days=gap)

        # Today's session
        today_session = None
        for s in all_sessions:
            if s["date"] == str(today):
                today_session = s
                break
        if today_session is None:
            for s in all_sessions:
                if s["date"] >= str(today) and s["session_id"] not in log:
                    today_session = s
                    break

        # Progress
        completed_sessions = [s for s in all_sessions if log.get(s["session_id"], {}).get("completed")]
        total_completed = len(completed_sessions)
        overall_progress = int((total_completed / total_sessions) * 100)
        current_week = today_session["week"] if today_session else 4
        week_sessions = [s for s in all_sessions if s["week"] == current_week]
        week_completed = len([s for s in week_sessions if log.get(s["session_id"], {}).get("completed")])
        week_progress = int((week_completed / len(week_sessions)) * 100) if week_sessions else 0
        total_score = sum(log.get(s["session_id"], {}).get("score", 0) for s in all_sessions)

        # ---- Program Complete ----
        if total_completed >= total_sessions:
            st.balloons()
            st.success("🏆 YOU COMPLETED YOUR 4-WEEK PROGRAM! ABSOLUTE BEAST MODE!")
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Sessions Done", f"{total_completed}/{total_sessions}")
            col2.metric("🏆 Final Score", f"{total_score}")
            col3.metric("📅 Days of Grinding", str(days_elapsed))
            st.divider()
            if st.button("🚀 Generate New Plan", use_container_width=True):
                archive_plan(user_id, plan, log)
                delete_plan(user_id)
                st.rerun()
            return

        # ---- Tabs ----
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📋 Full Program", "🍽️ Diet Plan", "💡 Tips"])

        # ---- DASHBOARD ----
        with tab1:
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

            # Plan Options
            with st.expander("⚙️ Plan Options"):
                st.warning("This will delete your current plan but keep all your progress history.")
                if st.button("🔄 Generate New Plan", use_container_width=True):
                    archive_plan(user_id, plan, log)
                    delete_plan(user_id)
                    st.rerun()

            st.divider()

            # Today's Workout
            st.subheader("💪 Today's Workout")

            glossary = {
                "rpe": "RPE = Rate of Perceived Exertion. Scale 1-10. RPE 7 = 3 more reps in tank. RPE 8 = 2 more. RPE 9 = 1 more. RPE 10 = absolute max.",
                "sets": "Sets = how many times you repeat a group of reps. 3 sets means do the exercise 3 times with rest in between.",
                "reps": "Reps = Repetitions. How many times you lift in one set.",
                "rdl": "RDL = Romanian Deadlift. Hinge at hips with slight knee bend. Great for hamstrings.",
                "ohp": "OHP = Overhead Press. Press barbell from shoulders straight overhead.",
                "amrap": "AMRAP = As Many Reps As Possible. Do as many reps as you can with good form.",
                "deload": "Deload = A lighter week to let your body recover and come back stronger.",
            }

            def show_exercise(ex):
                c1, c2 = st.columns([6, 1])
                with c1:
                    st.markdown(f"> **{ex['name']}** — {ex['sets']} sets × {ex['reps']} reps @ RPE {ex['rpe']}  \n> *{ex['note']}*")
                with c2:
                    relevant = [t for t in glossary if t in f"{ex['name']} {ex['note']} rpe sets reps".lower()]
                    if relevant:
                        with st.popover("💡"):
                            st.markdown("**📖 Quick Glossary**")
                            for term in relevant:
                                st.markdown(f"**{term.upper()}** — {glossary[term]}")

            if today_session:
                session_id = today_session["session_id"]
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

                    with st.form("session_log_form"):
                        completed = st.checkbox("✅ I completed this workout!")

                        exercise_names = [ex["name"].lower() for ex in today_session["exercises"]]
                        has_squat = any("squat" in e for e in exercise_names)
                        has_bench = any("bench" in e for e in exercise_names)
                        has_deadlift = any("deadlift" in e or "rdl" in e for e in exercise_names)

                        active_lifts = []
                        if has_squat: active_lifts.append("squat")
                        if has_bench: active_lifts.append("bench")
                        if has_deadlift: active_lifts.append("deadlift")

                        w_squat, w_bench, w_deadlift = 0, 0, 0
                        if active_lifts:
                            lift_cols = st.columns(len(active_lifts))
                            for i, lift in enumerate(active_lifts):
                                with lift_cols[i]:
                                    if lift == "squat":
                                        w_squat = st.number_input("🦵 Squat (kg)", min_value=0)
                                    elif lift == "bench":
                                        w_bench = st.number_input("💪 Bench (kg)", min_value=0)
                                    elif lift == "deadlift":
                                        w_deadlift = st.number_input("⚡ Deadlift (kg)", min_value=0)

                        rpe_felt = st.slider("😤 How hard did it feel? (RPE)", 1, 10, 7)
                        notes = st.text_input("📝 Notes (optional)")

                        log_submitted = st.form_submit_button("💾 Save Session", use_container_width=True)

                    if log_submitted:
                        weights_entered = (w_squat + w_bench + w_deadlift) > 0
                        score = calculate_score(completed, rpe_felt, weights_entered)
                        entry = {
                            "completed": completed,
                            "squat": w_squat,
                            "bench": w_bench,
                            "deadlift": w_deadlift,
                            "rpe": rpe_felt,
                            "notes": notes,
                            "score": score,
                            "date": str(today)
                        }
                        save_log_entry(user_id, session_id, entry)
                        st.success(f"🔥 Session logged! Score: **{score}/100**")
                        st.rerun()
            else:
                st.info("🛌 Rest day today! Recovery is part of the program.")

            st.divider()
            st.subheader("📅 Full Schedule")
            for s in all_sessions:
                sid = s["session_id"]
                s_log = log.get(sid, {})
                is_completed = s_log.get("completed", False)
                is_today = s["date"] == str(today)
                score = s_log.get("score", 0)
                icon = "👉" if is_today else ("✅" if is_completed else ("❌" if s["date"] < str(today) else "⬜"))
                label = f"{icon} **Week {s['week']} — {s['label']}** ({s['date']})"
                if is_completed:
                    label += f" — Score: {score}/100"
                st.markdown(label)

        # ---- FULL PROGRAM ----
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

        # ---- DIET ----
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

        # ---- TIPS ----
        with tab4:
            st.subheader("💡 Coach's Tips")
            for i, tip in enumerate(plan["tips"], 1):
                st.info(f"💡 **Tip {i}:** {tip}")

load_css()

# ================================================
# ROUTER — Check if logged in
# ================================================
if "user" not in st.session_state:
    try:
        # Try to get existing session
        user_data = get_user()
        if user_data:
            st.session_state["user"] = user_data.user
    except:
        pass

    # Check URL params for access token (Google OAuth redirect)
    params = st.query_params
    if "access_token" in params:
        try:
            session = supabase.auth.set_session(
                params["access_token"],
                params.get("refresh_token", "")
            )
            if session and session.user:
                st.session_state["user"] = session.user
                st.query_params.clear()
                st.rerun()
        except Exception as e:
            st.error(f"Login error: {e}")

if "user" in st.session_state and st.session_state["user"]:
    show_app(st.session_state["user"])
else:
    show_login()