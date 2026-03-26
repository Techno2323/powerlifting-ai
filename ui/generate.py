import streamlit as st
import json
from datetime import date
import google.generativeai as genai
from database import save_plan

def show_generate(user_id):
    st.markdown("""
    <div class="gen-header">
        <h2 class="gen-title">⚡ BUILD YOUR PROGRAM</h2>
        <p class="gen-subtitle">Enter your current maxes to get started</p>
        <div class="gen-cards">
            <div class="gen-card">
                <span class="gen-card-icon">🦵</span>
                <div class="gen-card-name">SQUAT</div>
                <div class="gen-card-sub">Enter below</div>
            </div>
            <div class="gen-card">
                <span class="gen-card-icon">💪</span>
                <div class="gen-card-name">BENCH</div>
                <div class="gen-card-sub">Enter below</div>
            </div>
            <div class="gen-card">
                <span class="gen-card-icon">⚡</span>
                <div class="gen-card-name">DEADLIFT</div>
                <div class="gen-card-sub">Enter below</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("user_form"):
        # Row 1 — Main lifts
        col1, col2, col3 = st.columns(3)
        with col1:
            squat     = st.number_input("🦵 Squat Max (kg)",    min_value=0)
        with col2:
            bench     = st.number_input("💪 Bench Max (kg)",    min_value=0)
        with col3:
            deadlift  = st.number_input("⚡ Deadlift Max (kg)", min_value=0)

        # Row 2 — Body stats
        col4, col5, col6 = st.columns(3)
        with col4:
            bodyweight = st.number_input("⚖️ Bodyweight (kg)", min_value=0)
        with col5:
            age        = st.number_input("🎂 Age", min_value=10, max_value=80)
        with col6:
            food       = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

        # Row 3 — Program settings
        col7, col8 = st.columns(2)
        with col7:
            goal = st.selectbox("🎯 Your Goal", ["Build Strength", "Bulk", "Cut"])
        with col8:
            days = st.selectbox("📅 Training Days/Week", [3, 4, 5, 6])

        submitted = st.form_submit_button("🚀 GENERATE MY PLAN", use_container_width=True)

    if submitted:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are an elite powerlifting coach with 20 years of experience coaching Indian athletes.

        Athlete profile:
        - Squat 1RM: {squat}kg
        - Bench 1RM: {bench}kg
        - Deadlift 1RM: {deadlift}kg
        - Bodyweight: {bodyweight}kg
        - Age: {age} years
        - Goal: {goal}
        - Training days per week: {days}
        - Diet preference: {food}

        PROGRAMMING RULES:
        1. Calculate exact training weights using percentages of their 1RM:
           - Week 1: 70-75% of 1RM (technique focus)
           - Week 2: 75-80% of 1RM (building)
           - Week 3: 80-87.5% of 1RM (peaking)
           - Week 4: 60-65% of 1RM (deload)
        2. Round all weights to nearest 2.5kg
        3. Design the program intelligently based on {days} training days:
           - Not every day needs the main competition lifts
           - Include heavy days, moderate days and recovery/accessory days smartly
           - Heavy days: main competition lift + 4-5 accessories
           - Moderate days: secondary lift + 4-5 volume accessories
           - Recovery days: light technique work + mobility focused accessories
        4. Each training day must have MINIMUM 5 exercises and MAXIMUM 7 exercises
        5. Choose powerlifting specific accessories:
           - Squat: pause squats, box squats, leg press, good mornings, RDL, leg curls
           - Bench: close grip bench, overhead press, dips, tricep pushdowns, face pulls, rows
           - Deadlift: rack pulls, deficit deadlifts, barbell rows, lat pulldowns, good mornings
        6. Adjust for age {age} — if over 35 add more recovery days and reduce peak intensity
        7. Calculate calories accurately:
           - TDEE = bodyweight {bodyweight} x 33 (active person)
           - Add 200-300 for bulking, subtract 300-400 for cutting, maintain for strength
           - Protein minimum = bodyweight x 2.2g
        8. Every exercise must have a specific weight in kg based on their lifts
        9. Write coaching notes that are specific and actionable
        10. Diet must use ONLY Indian foods for {food} preference with at least 6 meals

        Return ONLY valid JSON, no markdown, no backticks, no extra text.
        {{
            "summary": "2 sentence personalized summary mentioning their actual squat/bench/deadlift numbers",
            "goal": "{goal}",
            "training_days": {days},
            "weeks": [
                {{
                    "week": 1,
                    "focus": "specific focus for week 1",
                    "days": [
                        {{
                            "day_number": 1,
                            "label": "Day 1 - Heavy Squat",
                            "exercises": [
                                {{
                                    "name": "Squat",
                                    "sets": 4,
                                    "reps": "5",
                                    "weight": "specific kg based on their 1RM",
                                    "rpe": "7",
                                    "note": "specific coaching cue for this athlete"
                                }}
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
                        "food": "specific Indian meal with quantities",
                        "protein": 35,
                        "carbs": 60,
                        "fats": 20
                    }}
                ]
            }},
            "tips": [
                "specific tip based on their squat to deadlift ratio",
                "specific tip based on their age and recovery",
                "specific tip based on their goal and bodyweight"
            ]
        }}

        Generate ALL 4 weeks completely with {days} training days each week.
        Every single exercise must have a specific weight in kg.
        Minimum 5 exercises per day, maximum 7.
        Make it feel like a real coach wrote this specifically for this athlete.
        """

        with st.spinner("Building your personalized plan... 🔥"):
            try:
                response = model.generate_content(prompt)
                raw = response.text.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                raw = raw.strip()
                data = json.loads(raw)
                data["start_date"]    = str(date.today())
                data["training_days"] = days
                save_plan(user_id, data)
                st.success("✅ Plan generated!")
                st.balloons()
                st.rerun()
            except json.JSONDecodeError as e:
                st.error("❌ Failed to parse plan. Please try again.")
                st.code(str(e))
            except Exception as e:
                st.error(f"❌ Error: {e}")