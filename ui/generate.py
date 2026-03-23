import streamlit as st
import json
from datetime import date
import google.generativeai as genai
from groq import Groq
from database import save_plan, supabase

def show_generate(user_id):
    st.markdown("""<div style="background:linear-gradient(135deg,#1a1a1a,#111);border:1px solid #FFD70033;border-radius:20px;padding:35px 40px;margin:20px 0;box-shadow:0 0 40px #FFD70011;">
    <h2 style="text-align:center;color:#FFD700;font-family:Rajdhani,sans-serif;">⚡ BUILD YOUR PROGRAM</h2>
    <p style="text-align:center;color:#888;font-size:0.9rem;text-transform:uppercase;letter-spacing:2px;">Enter your current maxes to get started</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-top:20px;">
    <div style="background:#0d0d0d;border:1px solid #FFD70033;border-radius:16px;padding:25px;text-align:center;">
    <div style="font-size:2.5rem;">🦵</div><div style="color:#FFD700;font-weight:700;letter-spacing:2px;">SQUAT</div>
    <div style="color:#555;font-size:0.75rem;">Enter below</div></div>
    <div style="background:#0d0d0d;border:1px solid #FFD70033;border-radius:16px;padding:25px;text-align:center;">
    <div style="font-size:2.5rem;">💪</div><div style="color:#FFD700;font-weight:700;letter-spacing:2px;">BENCH</div>
    <div style="color:#555;font-size:0.75rem;">Enter below</div></div>
    <div style="background:#0d0d0d;border:1px solid #FFD70033;border-radius:16px;padding:25px;text-align:center;">
    <div style="font-size:2.5rem;">⚡</div><div style="color:#FFD700;font-weight:700;letter-spacing:2px;">DEADLIFT</div>
    <div style="color:#555;font-size:0.75rem;">Enter below</div></div>
    </div></div>""", unsafe_allow_html=True)

    with st.form("user_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            squat = st.number_input("🦵 Squat Max (kg)", min_value=0)
        with col2:
            bench = st.number_input("💪 Bench Max (kg)", min_value=0)
        with col3:
            deadlift = st.number_input("⚡ Deadlift Max (kg)", min_value=0)

        col4, col5, col6 = st.columns(3)
        with col4:
            goal = st.selectbox("🎯 Your Goal", ["Build Strength", "Bulk", "Cut"])
        with col5:
            days = st.selectbox("📅 Training Days/Week", [3, 4, 5, 6])
        with col6:
            food = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

        submitted = st.form_submit_button("🚀 GENERATE MY PLAN", use_container_width=True)

    if submitted:
        model = genai.GenerativeModel("gemini-2.5-flash")
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
                raw = raw.strip()
                data = json.loads(raw)
                data["start_date"] = str(date.today())
                data["training_days"] = days
                save_plan(user_id, data)
                st.success("✅ Plan generated!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")