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
    """
    Robustly extract JSON from Gemini response with truncation recovery.
    Handles:
    - Markdown code fences (```json ... ```)
    - Trailing text after JSON closes
    - Incomplete/truncated responses
    - Auto-closing incomplete JSON structures
    
    Returns: parsed dict or raises ValueError with preview.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response from AI: contents must not be empty. Try again or adjust your athlete profile.")
    
    # Remove markdown code fences
    text = re.sub(r'```(?:json)?\s*\n?', '', raw_text).strip()
    text = re.sub(r'\n```\s*$', '', text).strip()
    
    # Find the first { and last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        preview = text[:200] if len(text) > 200 else text
        raise ValueError(
            f"No valid JSON object found in response.\n"
            f"Response preview: {preview}\n"
            f"Ensure the AI response contains a complete JSON object."
        )
    
    json_str = text[start_idx:end_idx+1]
    
    try:
        parsed = json.loads(json_str)
        return parsed
    except json.JSONDecodeError as e:
        # Try to recover from truncation by auto-closing structures
        st.warning(f"⚠️ JSON truncation detected at position {e.pos}. Attempting recovery...")
        
        recovery_attempts = [
            # Attempt 1: Close all open arrays and objects
            lambda s: s + "]" * s.count("[") + "}" * s.count("{"),
            # Attempt 2: Find last complete array/object and close from there
            lambda s: _recover_truncated_json(s),
        ]
        
        for attempt_fn in recovery_attempts:
            try:
                recovered = attempt_fn(json_str)
                parsed = json.loads(recovered)
                st.info(f"✅ JSON recovered successfully (auto-closed incomplete structure)")
                return parsed
            except json.JSONDecodeError:
                continue
        
        # All recovery attempts failed
        preview = json_str[:300] if len(json_str) > 300 else json_str
        raise ValueError(
            f"Invalid JSON syntax at position {e.pos}.\n"
            f"Error: {e.msg}\n"
            f"JSON preview: {preview}\n"
            f"The response may be incomplete. Try regenerating with a simpler athlete profile or fewer days/week."
        )


def _recover_truncated_json(json_str: str) -> str:
    """
    Attempt to recover truncated JSON by finding last complete object/array
    and closing all open structures.
    """
    # Count open/close brackets
    open_braces = json_str.count('{') - json_str.count('}')
    open_brackets = json_str.count('[') - json_str.count(']')
    
    # Add closing brackets
    recovered = json_str + '}' * open_braces + ']' * open_brackets
    return recovered


def normalize_plan_schema(data: dict, training_days: int) -> dict:
    """
    Normalize generated plan to match dashboard expectations.
    Maps nested "program.weeks" -> top-level "weeks".
    Ensures required keys exist.
    
    Returns: normalized plan_data dict.
    """
    # Unnest if AI returned nested structure
    if isinstance(data.get("program"), dict) and "weeks" in data["program"]:
        program = data.pop("program")
        data["weeks"] = program.get("weeks", [])
        if "diet" not in data:
            data["diet"] = program.get("diet", {})
        if "tips" not in data:
            data["tips"] = program.get("tips", [])
    
    # Ensure required top-level keys
    if "weeks" not in data or not isinstance(data.get("weeks"), list):
        raise ValueError("Plan missing 'weeks' list. Generated plan is invalid.")
    
    if not data["weeks"]:
        raise ValueError("Plan has zero weeks. Generated plan is empty.")
    
    if "diet" not in data:
        data["diet"] = {}
    
    if "tips" not in data:
        data["tips"] = []
    
    # Validate weeks structure (allow partial if truncated)
    for week in data["weeks"]:
        if "days" not in week or not isinstance(week.get("days"), list):
            # If weeks exist but no days, create empty day placeholder
            if "days" not in week:
                week["days"] = []
        if not week.get("days", []):
            # Warn but allow (better than crashing)
            st.warning(f"⚠️ Week {week.get('week', '?')} has no days (may be truncated)")
    
    # Add metadata
    data["training_days"] = training_days
    data["start_date"] = str(date.today())
    
    return data


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
        # STEP 1: Generate training plan from Gemini AI
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

                # Call Gemini API with optimized settings for streaming
                model = genai.GenerativeModel(GEMINI_MODEL)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=GEMINI_TEMPERATURE,
                        top_p=GEMINI_TOP_P,
                        max_output_tokens=GEMINI_MAX_TOKENS,
                    ),
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_NONE",
                        },
                    ]
                )
                
                raw = response.text.strip() if response.text else ""
                
                if not raw:
                    raise ValueError("Gemini returned empty response. Try again with different inputs.")
                
                # ============================================================
                # STEP 2: Extract and parse JSON robustly
                # ============================================================
                data = extract_and_parse_json(raw)
                
                # ============================================================
                # STEP 3: Normalize schema
                # ============================================================
                data = normalize_plan_schema(data, int(days))
                
                # ============================================================
                # STEP 4: Expand training plan with exercises
                # ============================================================
                data = expand_minimal_json(data, int(days))

                # ============================================================
                # STEP 5: Generate diet plan
                # ============================================================
                diet_data = generate_diet_plan(
                    bodyweight=int(bodyweight),
                    goal=goal,
                    diet_type=food,
                    data=data
                )
                data["diet"] = diet_data
                
                # ============================================================
                # STEP 6: Save complete plan to database
                # ============================================================
                save_plan(user_id, data)
                
                st.success("✅ Plan generated successfully!")
                st.balloons()
                import time
                time.sleep(1)
                st.rerun()
                
            except ValueError as e:
                st.error(f"❌ Invalid plan generated: {str(e)}")
                with st.expander("📋 Troubleshooting"):
                    st.write("This might happen if:")
                    st.write("- The AI response was incomplete or truncated")
                    st.write("- The prompt was too complex for Gemini 2.5 Flash Lite")
                    st.write("- Your athlete profile has extreme values")
                    st.write("\n**Try one of these:**")
                    st.write("1. Reduce training days/week (e.g., try 3 instead of 6)")
                    st.write("2. Use rounder numbers for lifts/bodyweight")
                    st.write("3. Wait a moment and try again (rate limiting)")
                    st.write("4. Contact support if this persists")
            except json.JSONDecodeError as e:
                st.error("❌ Failed to parse AI response as JSON")
                with st.expander("📋 Error Details"):
                    st.write(f"**JSON Error:** {str(e)}")
                    st.write("The AI response was truncated or malformed. Try regenerating.")
            except Exception as e:
                st.error(f"❌ Error generating plan: {str(e)}")
                with st.expander("📋 Technical Details"):
                    st.write(f"**Exception:** {type(e).__name__}")
                    st.write(f"**Message:** {str(e)}")
                    st.write("If this persists, try:")
                    st.write("- Simpler athlete profile (fewer days, rounder numbers)")
                    st.write("- Contact support with this error message")