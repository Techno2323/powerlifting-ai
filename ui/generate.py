"""
Simplified Generate UI using unified AI engine
Now with Powerbuilding goal support!
"""

import streamlit as st
import json
from datetime import date
from database import save_plan
from ai_engine import generate_program
from config import DEBUG


def show_generate(user_id):
    """Display the program generation form"""
    
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

    # ========== FORM ==========
    with st.form("user_form"):
        st.subheader("💪 Your Lifts")
        col1, col2, col3 = st.columns(3)
        with col1:
            squat = st.number_input("🦵 Squat Max (kg)", min_value=0, value=100)
        with col2:
            bench = st.number_input("💪 Bench Max (kg)", min_value=0, value=70)
        with col3:
            deadlift = st.number_input("⚡ Deadlift Max (kg)", min_value=0, value=140)

        st.subheader("📊 Your Stats")
        col4, col5, col6 = st.columns(3)
        with col4:
            bodyweight = st.number_input("⚖️ Bodyweight (kg)", min_value=0, value=75)
        with col5:
            height = st.number_input("📏 Height (cm)", min_value=100, max_value=220, value=175)
        with col6:
            age = st.number_input("🎂 Age", min_value=10, max_value=80, value=25)

        st.subheader("🎯 Your Goals")
        col7, col8 = st.columns(2)
        with col7:
            goal = st.selectbox("Goal", ["Build Strength", "Powerbuilding", "Bulk", "Cut"])
        with col8:
            food = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

        # ✨ Show goal explanation
        if goal == "Powerbuilding":
            st.info("💪 **Powerbuilding**: Maximize BOTH strength AND muscle mass. Heavy compounds (3-5 reps) + hypertrophy accessories (8-12 reps). Best of both worlds!")
        elif goal == "Build Strength":
            st.info("🔥 **Build Strength**: Focus on progressive overload. Heavy weights, low reps (1-5), maximum strength gains.")
        elif goal == "Bulk":
            st.info("📈 **Bulk**: Build muscle mass with caloric surplus. Higher volume, moderate weights (8-12 reps), muscle growth focus.")
        else:  # Cut
            st.info("⚖️ **Cut**: Lose fat while preserving muscle. Caloric deficit, high protein, strength maintenance (moderate reps).")

        st.subheader("⏰ Lifestyle")
        col9, col10 = st.columns(2)
        with col9:
            days = st.selectbox("Training Days/Week", [3, 4, 5, 6])
        with col10:
            activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Very Active"])

        submitted = st.form_submit_button("🚀 GENERATE MY PLAN", use_container_width=True)

    # ========== VALIDATION & GENERATION ==========
    if submitted:
        # Validate inputs
        if squat == 0 and bench == 0 and deadlift == 0:
            st.error("❌ Please enter at least one lift max.")
            return
        
        if bodyweight == 0:
            st.error("❌ Please enter your bodyweight.")
            return
        
        if height == 0:
            st.error("❌ Please enter your height.")
            return

        # Prepare user stats
        user_stats = {
            'squat': int(squat),
            'bench': int(bench),
            'deadlift': int(deadlift),
            'bodyweight': int(bodyweight),
            'height': int(height),
            'age': int(age),
            'goal': goal,
            'days': int(days),
            'food': food,
            'activity': activity
        }

        # Generate program
        with st.spinner("🔥 AI Coach is designing your personalized program..."):
            try:
                # ✨ ONE CALL = EVERYTHING!
                program_data = generate_program(user_stats)
                
                # Add metadata
                program_data["start_date"] = str(date.today())
                program_data["training_days"] = int(days)
                program_data["user_stats"] = user_stats
                
                # Save to database
                save_plan(user_id, program_data)
                
                st.success("✅ Plan generated successfully!")
                st.balloons()
                
                # Show preview
                with st.expander("📋 Program Preview"):
                    st.json(program_data)
                
                import time
                time.sleep(1)
                st.rerun()
                
            except ValueError as e:
                st.error(f"❌ Invalid input: {str(e)}")
                with st.expander("📋 Error Details"):
                    st.write(str(e))
            
            except Exception as e:
                st.error(f"❌ Error generating plan: {str(e)}")
                with st.expander("📋 Error Details"):
                    st.write(str(e))
                    if DEBUG:
                        st.write("**Debug Info:**")
                        st.write(f"User Stats: {user_stats}")