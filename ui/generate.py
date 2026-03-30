import streamlit as st
import json
import re
from datetime import date
from database import save_plan
from prompts import get_coaching_prompt
from json_builder import expand_minimal_json
from diet_builder import generate_diet_plan
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MAX_TOKENS, GEMINI_TEMPERATURE, GEMINI_TOP_P
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)


def extract_and_parse_json(raw_text: str) -> dict:
    """Robustly extract JSON from Gemini response with truncation recovery."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response from AI. Try again with different inputs.")
    
    # Remove markdown fences
    text = re.sub(r'```(?:json)?\s*\n?', '', raw_text).strip()
    text = re.sub(r'\n```\s*$', '', text).strip()
    
    # Find first { and last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        preview = text[:200] if len(text) > 200 else text
        raise ValueError(f"No valid JSON found. Response: {preview}")
    
    json_str = text[start_idx:end_idx+1]
    
    try:
        parsed = json.loads(json_str)
        return parsed
    except json.JSONDecodeError as e:
        # Try to recover truncated JSON
        st.warning(f"⚠️ JSON truncation detected at position {e.pos}. Attempting auto-recovery...")
        
        # Auto-close open structures
        open_braces = json_str.count('{') - json_str.count('}')
        open_brackets = json_str.count('[') - json_str.count(']')
        recovered = json_str + '}' * open_braces + ']' * open_brackets
        
        try:
            parsed = json.loads(recovered)
            st.info("✅ JSON recovered successfully!")
            return parsed
        except:
            preview = json_str[:300]
            raise ValueError(f"Invalid JSON at pos {e.pos}. Preview: {preview}")


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

        with st.spinner("🔥 AI Coach is designing your personalized program..."):
            try:
                # Generate prompt
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

                # **CRITICAL FIX**: Call Gemini API instead of Groq
                model = genai.GenerativeModel(GEMINI_MODEL)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=GEMINI_TEMPERATURE,
                        top_p=GEMINI_TOP_P,
                        max_output_tokens=GEMINI_MAX_TOKENS,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                    ]
                )
                
                raw = response.text.strip() if response.text else ""
                if not raw:
                    raise ValueError("Gemini returned empty response.")
                
                # Extract JSON (with truncation recovery)
                data = extract_and_parse_json(raw)
                
                # Expand program
                data = expand_minimal_json(data, int(days))
                
                # Validate structure
                if not data.get("weeks") or not isinstance(data.get("weeks"), list):
                    raise ValueError("Plan missing weeks list.")
                
                # Generate diet
                diet_data = generate_diet_plan(
                    bodyweight=int(bodyweight),
                    goal=goal,
                    diet_type=food,
                    data=data
                )
                data["diet"] = diet_data
                data["start_date"] = str(date.today())
                data["training_days"] = int(days)
                
                # Save plan
                save_plan(user_id, data)
                
                st.success("✅ Plan generated successfully!")
                st.balloons()
                import time
                time.sleep(1)
                st.rerun()
                
            except ValueError as e:
                st.error(f"❌ Invalid plan: {str(e)}")
                with st.expander("📋 Troubleshooting"):
                    st.write("**Try these steps:**")
                    st.write("1. Reduce training days to 3 (instead of 6)")
                    st.write("2. Use rounder numbers (100kg not 97kg)")
                    st.write("3. Wait a moment and try again")
                    st.write("4. Contact support if persistent")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("📋 Details"):
                    st.write(f"**Type:** {type(e).__name__}")
                    st.write(f"**Message:** {str(e)}")