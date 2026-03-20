import google.generativeai as genai
import streamlit as st
import json

genai.configure(api_key="AIzaSyCxqJ0jLDo_bMhZl8FUvVmdN4X1-wsyF6c")
model = genai.GenerativeModel("gemini-2.5-flash")

# ---- Page Config ----
st.set_page_config(page_title="Indian Powerlifting AI Coach", page_icon="🏋️", layout="wide")

st.title("🏋️ Indian Powerlifting AI Coach")
st.caption("Built for Indian athletes. Real food. Real strength.")

# ---- Input Form ----
with st.form("user_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        squat = st.number_input("🦵 Best Squat (kg)", min_value=0)
        bench = st.number_input("💪 Best Bench Press (kg)", min_value=0)
        deadlift = st.number_input("⚡ Best Deadlift (kg)", min_value=0)
    
    with col2:
        goal = st.selectbox("🎯 Your Goal", ["Build Strength", "Bulk", "Cut"])
        days = st.selectbox("📅 Training Days/Week", [3, 4, 5])
        food = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])
    
    submitted = st.form_submit_button("🚀 Generate My Plan", use_container_width=True)

# ---- AI Call ----
if submitted:
    prompt = f"""
    You are an expert powerlifting coach for Indian athletes.
    
    User stats:
    - Squat: {squat} kg, Bench: {bench} kg, Deadlift: {deadlift} kg
    - Goal: {goal}
    - Training days per week: {days}
    - Diet: {food}

    Return ONLY a valid JSON object with NO extra text, NO markdown, NO backticks.
    
    Use this exact structure:
    {{
        "summary": "2 line motivational summary for this athlete",
        "weeks": [
            {{
                "week": 1,
                "focus": "one line focus for this week",
                "days": [
                    {{
                        "day": "Day 1 - Squat Emphasis",
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
                    "food": "Paneer bhurji with 2 rotis and curd",
                    "protein": 35,
                    "carbs": 60,
                    "fats": 20
                }}
            ]
        }},
        "tips": ["tip 1", "tip 2", "tip 3"]
    }}
    
    Generate all 4 weeks with {days} training days each. Use Indian foods like dal, paneer, roti, rice, eggs, chicken based on {food} diet.
    """

    with st.spinner("Building your personalized plan... 🔥"):
        try:
            response = model.generate_content(prompt)
            raw = response.text.strip()
            
            # Clean JSON if model adds backticks
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            
            data = json.loads(raw)

            # ---- Display Summary ----
            st.success(data["summary"])

            # ---- Tabs ----
            tab1, tab2, tab3 = st.tabs(["💪 Training Program", "🍽️ Diet Plan", "💡 Tips"])

            # ---- Training Tab ----
            with tab1:
                for week in data["weeks"]:
                    st.subheader(f"Week {week['week']} — {week['focus']}")
                    
                    cols = st.columns(len(week["days"]))
                    for i, day in enumerate(week["days"]):
                        with cols[i]:
                            st.markdown(f"**{day['day']}**")
                            for ex in day["exercises"]:
                                st.markdown(f"""
                                > **{ex['name']}**  
                                > {ex['sets']} sets × {ex['reps']} reps @ RPE {ex['rpe']}  
                                > *{ex['note']}*
                                """)
                    st.divider()

            # ---- Diet Tab ----
            with tab2:
                # Macro Summary
                diet = data["diet"]
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🔥 Calories", f"{diet['calories']} kcal")
                m2.metric("🥩 Protein", f"{diet['protein']}g")
                m3.metric("🍚 Carbs", f"{diet['carbs']}g")
                m4.metric("🥑 Fats", f"{diet['fats']}g")
                
                st.divider()
                
                # Meals
                for meal in diet["meals"]:
                    with st.expander(f"🕐 {meal['time']} — {meal['name']}"):
                        st.write(f"**{meal['food']}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Protein", f"{meal['protein']}g")
                        c2.metric("Carbs", f"{meal['carbs']}g")
                        c3.metric("Fats", f"{meal['fats']}g")

            # ---- Tips Tab ----
            with tab3:
                for i, tip in enumerate(data["tips"], 1):
                    st.info(f"💡 **Tip {i}:** {tip}")

        except json.JSONDecodeError:
            st.error("AI returned unexpected format. Try again!")
        except Exception as e:
            st.error(f"Error: {e}")