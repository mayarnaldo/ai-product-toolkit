import streamlit as st
import json
from llm_client import ask_ai
from prompts import build_prompt

# ---------------------------------------------------------
# Safe JSON Parser
# ---------------------------------------------------------
def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        return None

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("🧩 Workflow Assistant")

# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------
st.title("🧩 Workflow Assistant")
st.caption("Turn user stories into structured product artifacts.")

st.markdown("---")

# ---------------------------------------------------------
# Session State Setup
# ---------------------------------------------------------
if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

# ---------------------------------------------------------
# Input Section
# ---------------------------------------------------------
st.subheader("📝 User Story Input")

user_story = st.text_area(
    "Enter your user story",
    placeholder="As a user, I want to..."
)

analyze_clicked = st.button("🔍 Generate Workflow")

st.markdown("---")

# ---------------------------------------------------------
# Analyze Logic
# ---------------------------------------------------------
if analyze_clicked:
    if not user_story.strip():
        st.error("Please enter a user story before generating.")
    else:
        with st.spinner("Analyzing user story..."):
            prompt = build_prompt(user_story)
            raw = ask_ai(prompt)

            parsed = safe_json_parse(raw)

            if parsed is None:
                st.error("The AI returned invalid JSON. Showing raw output:")
                st.code(raw)
            else:
                st.session_state.workflow_result = parsed

# ---------------------------------------------------------
# Output Section
# ---------------------------------------------------------
if st.session_state.workflow_result:
    result = st.session_state.workflow_result

    st.subheader("📋 Workflow Output")

    # Acceptance Criteria
    st.markdown("### ✅ Acceptance Criteria")
    for item in result.get("acceptance_criteria", []):
        st.markdown(f"- {item}")

    # Workflow Steps
    st.markdown("### 🔄 Workflow Steps")
    for step in result.get("workflow_steps", []):
        st.markdown(f"1. {step}")

    # Risks
    st.markdown("### ⚠️ Risks & Dependencies")
    for risk in result.get("risks", []):
        st.markdown(f"- {risk}")

    # Test Cases
    st.markdown("### 🧪 Test Cases")
    for test in result.get("test_cases", []):
        st.markdown(f"- {test}")

    # Metrics
    st.markdown("### 📊 Success Metrics")
    for metric in result.get("metrics", []):
        st.markdown(f"- {metric}")

    st.button("📋 Copy Workflow Summary")

else:
    st.info("No results yet. Enter a user story and click **Generate Workflow**.")
