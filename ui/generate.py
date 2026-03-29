import streamlit as st
import json
import re
from datetime import date
from database import save_plan
from prompts import get_coaching_prompt
from json_builder import expand_minimal_json
from diet_builder import generate_diet_plan
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE

def clean_json_response(raw_text):
    """Clean AI response"""
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(1).strip()
    brace_index = raw_text.find('{')
    if brace_index > 0:
        raw_text = raw_text[brace_index:]
    last_brace = raw_text.rfind('}')
    if last_brace != -1:
        raw_text = raw_text[:last_brace + 1]
    return raw_text.strip()

def show_generate(user_id):
    st.markdown("""
    <style>
    @media (max-width: 640px) {
        [data-testid="stForm"] [data-testid="stHorizontalBlock"] {
            gap: 6px !important;
        }
        [data-testid="stFormSubmitButton"] button {
            min-height: 56px !important;
            font-size: 1.1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gen-header">
        <h2 class="gen-title">⚡ BUILD YOUR PROGRAM</h2>
        <p class="gen-subtitle">Enter your stats to get a personalized plan</p>
    </div>
    """, unsafe_allow_html=True)

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
            bodyweight = st.number_input("⚖️ Bodyweight (kg)", min_value=0)
        with col5:
            height = st.number_input("📏 Height (cm)", min_value=100, max_value=220)
        with col6:
            age = st.number_input("🎂 Age", min_value=10, max_value=80)

        col7, col8 = st.columns(2)
        with col7:
            goal = st.selectbox("🎯 Your Goal", ["Build Strength", "Bulk", "Cut"])
        with col8:
            food = st.selectbox("🍽️ Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

        col9, col10 = st.columns(2)
        with col9:
            days = st.selectbox("📅 Training Days/Week", [3, 4, 5, 6])
        with col10:
            activity = st.selectbox("🏃 Activity Level", ["Sedentary", "Light", "Moderate", "Very Active"])

        submitted = st.form_submit_button("🚀 GENERATE MY PLAN", use_container_width=True)

    if submitted:
        # Validation
        if squat == 0 and bench == 0 and deadlift == 0:
            st.error("❌ Please enter at least one lift max.")
            st.stop()
        
        if bodyweight == 0:
            st.error("❌ Please enter your bodyweight.")
            st.stop()
        
        if height == 0:
            st.error("❌ Please enter your height.")
            st.stop()

        # ============================================================
        # STEP 1: Generate training plan from Groq AI
        # ============================================================
        with st.spinner("🔥 AI Coach is designing your personalized program..."):
            try:
                # Generate prompt for training plan
                prompt = get_coaching_prompt(
                    squat=int(squat),
                    bench=int(bench),
                    deadlift=int(deadlift),
                    bodyweight=int(bodyweight),
                    height=int(height),
                    age=int(age),
                    goal=goal,
                    days=int(days),
                    food=food,
                    activity=activity
                )

                # Call Groq API
                from groq import Groq
                
                client = Groq(api_key=GROQ_API_KEY)
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "Return ONLY valid JSON. No markdown, no backticks."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=GROQ_TEMPERATURE,
                    max_tokens=GROQ_MAX_TOKENS,
                )
                
                raw = response.choices[0].message.content.strip()
                cleaned = clean_json_response(raw)
                
                # Parse training plan JSON
                data = json.loads(cleaned)
                
                # ============================================================
                # STEP 2: Expand training plan with exercises
                # ============================================================
                data = expand_minimal_json(data, int(days))

                if not isinstance(data, dict) or not data.get("weeks"):
                    raise ValueError("Generated plan is missing training weeks. Please try again.")

                if not isinstance(data.get("diet"), dict):
                    data["diet"] = {}
                
                # ============================================================
                # STEP 3: Calculate calorie needs
                # ============================================================
                # Mifflin-St Jeor equation for maintenance
                maintenance = (10 * int(bodyweight)) + (6.25 * int(height)) - (5 * int(age)) + 5
                
                # Apply activity level multiplier
                activity_multipliers = {
                    "Sedentary": 1.2,
                    "Light": 1.375,
                    "Moderate": 1.55,
                    "Very Active": 1.725
                }
                
                tdee = maintenance * activity_multipliers.get(activity, 1.55)
                
                # Adjust for goal
                if goal == "Build Strength":
                    calories = int(tdee + 300)  # +300 cal surplus
                elif goal == "Bulk":
                    calories = int(tdee + 500)  # +500 cal surplus
                else:  # Cut
                    calories = int(tdee - 500)  # -500 cal deficit
                
                # Calculate macros
                protein = int(int(bodyweight) * 2.2)
                carbs = int(int(bodyweight) * 5.5)
                fats = int(int(bodyweight) * 1.1)
                
                # ============================================================
                # STEP 4: Generate personalized diet with alternatives
                # ============================================================
                selected_meals, meal_macros, meal_alternatives = generate_diet_plan(
                    bodyweight=int(bodyweight),
                    height=int(height),
                    age=int(age),
                    goal=goal,
                    food_type=food,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fats=fats
                )
                
                # Convert selected meals to list format for storage
                meals_list = []
                for time, meal in selected_meals.items():
                    meal_copy = meal.copy()
                    time_parts = time.split(" ")
                    meal_copy["time"] = f"{time_parts[0]} {time_parts[1]}"
                    meal_copy["name"] = " ".join(time_parts[2:])
                    meals_list.append(meal_copy)
                
                # ============================================================
                # STEP 5: Update diet data in plan
                # ============================================================
                data["diet"]["meals"] = meals_list
                data["diet"]["calories"] = calories
                data["diet"]["protein"] = protein
                data["diet"]["carbs"] = carbs
                data["diet"]["fats"] = fats
                data["diet"]["maintenance"] = int(maintenance)
                data["diet"]["tdee"] = int(tdee)
                data["diet"]["meal_alternatives"] = meal_alternatives
                
                # ============================================================
                # STEP 6: Add program metadata
                # ============================================================
                data["start_date"] = str(date.today())
                data["training_days"] = int(days)
                
                # ============================================================
                # STEP 7: Save complete plan to database
                # ============================================================
                save_plan(user_id, data)
                
                st.success("✅ Plan generated successfully!")
                st.balloons()
                import time
                time.sleep(1)
                st.rerun()
                
            except json.JSONDecodeError as e:
                st.error("❌ Failed to parse plan - Invalid JSON response")
                with st.expander("📋 Error Details"):
                    st.write(f"**Error:** {str(e)}")
                    st.write("This might be because:")
                    st.write("- The AI response was incomplete")
                    st.write("- The prompt was too complex")
                    st.write("Try again or adjust your inputs")
            except Exception as e:
                st.error(f"❌ Error generating plan: {str(e)}")
                with st.expander("📋 Error Details"):
                    st.write(str(e))