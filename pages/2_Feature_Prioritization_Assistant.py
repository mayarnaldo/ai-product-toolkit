import streamlit as st
import json
from llm_client import ask_ai

# -----------------------------
# Sidebar Title
# -----------------------------
st.sidebar.title("🧭 Feature Prioritization Assistant")

# -----------------------------
# Page Header
# -----------------------------
st.title("📌 Feature Prioritization Assistant")
st.caption("Make prioritization transparent, structured, and explainable.")

st.markdown("---")

# -----------------------------
# Session State Setup
# -----------------------------
if "clarifying_questions" not in st.session_state:
    st.session_state.clarifying_questions = None

if "prioritization_result" not in st.session_state:
    st.session_state.prioritization_result = None

# -----------------------------
# Input Section
# -----------------------------
st.subheader("📝 Input Area")

feature_ideas = st.text_area(
    "Feature Ideas",
    placeholder="List your feature ideas here, one per line..."
)

user_feedback = st.text_area(
    "User Feedback (Optional)",
    placeholder="Paste relevant user feedback, quotes, or insights..."
)

framework = st.selectbox(
    "Choose a Prioritization Framework",
    ["RICE", "Value vs Effort", "MoSCoW", "Custom (AI-guided)"]
)

analyze_clicked = st.button("🔍 Analyze & Prioritize")

st.markdown("---")

# -----------------------------
# Clarifying Questions Section
# -----------------------------
if st.session_state.clarifying_questions:
    st.subheader("❓ Clarifying Questions")

    answers = {}
    for q in st.session_state.clarifying_questions:
        answers[q] = st.text_input(q)

    submit_answers = st.button("Submit Answers")

    if submit_answers:
        # Build follow-up prompt
        followup_prompt = f"""
        The user has answered your clarifying questions. 
        Use these answers to finalize the prioritization.

        Answers:
        {json.dumps(answers, indent=2)}
        """

        raw = ask_ai(followup_prompt)

        try:
            result = json.loads(raw)
            st.session_state.prioritization_result = result
            st.session_state.clarifying_questions = None
        except:
            st.error("The AI returned invalid JSON. Showing raw output:")
            st.code(raw)

# -----------------------------
# Analyze Button Logic
# -----------------------------
if analyze_clicked:
    if not feature_ideas.strip():
        st.error("Please enter at least one feature idea.")
    else:
        with st.spinner("Analyzing features..."):
            prompt = f"""
            You are an AI Feature Prioritization Assistant.

            Feature ideas:
            {feature_ideas}

            User feedback (optional):
            {user_feedback}

            Framework selected: {framework}

            Your tasks:
            1. If needed, generate clarifying questions as a JSON list under "clarifying_questions".
            2. If enough information is provided, return:
                - "ranked_features": a ranked list of features
                - "explanations": reasoning behind the ranking

            Respond ONLY in JSON.
            """

            raw = ask_ai(prompt)

            try:
                data = json.loads(raw)

                # If AI wants more info
                if "clarifying_questions" in data:
                    st.session_state.clarifying_questions = data["clarifying_questions"]
                    st.info("The AI needs more information. Please answer the questions below.")

                # If AI already produced results
                if "ranked_features" in data:
                    st.session_state.prioritization_result = data

            except:
                st.error("The AI returned invalid JSON. Showing raw output:")
                st.code(raw)

# -----------------------------
# Prioritized Roadmap Section
# -----------------------------
if st.session_state.prioritization_result:
    st.subheader("📊 Prioritized Roadmap")

    result = st.session_state.prioritization_result

    # Ranked Feature List
    st.markdown("### 🥇 Ranked Feature List")
    for item in result.get("ranked_features", []):
        st.markdown(f"- **{item}**")

    # Explanations
    st.markdown("### 🧠 Why These Rankings?")
    for explanation in result.get("explanations", []):
        st.markdown(f"- {explanation}")

    # Copy Button
    st.button("📋 Copy Roadmap")

else:
    st.info("No results yet. Add your features and click **Analyze & Prioritize**.")