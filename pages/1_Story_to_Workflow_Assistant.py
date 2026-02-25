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

if "run_workflow" not in st.session_state:
    st.session_state.run_workflow = False

if "user_story" not in st.session_state:
    st.session_state.user_story = ""

# ---------------------------------------------------------
# Input Section
# ---------------------------------------------------------
st.subheader("📝 User Story Input")

# Persist user story across reruns
user_story_input = st.text_area(
    "Enter your user story",
    value=st.session_state.user_story,
    placeholder="As a user, I want to..."
)

# Always keep latest text in session_state
st.session_state.user_story = user_story_input

# DEBUG: show what we are actually sending
st.caption("🔎 Debug – current user story value:")
st.code(st.session_state.user_story or "<EMPTY>", language="text")

# Button that triggers workflow generation
if st.button("🔍 Generate Workflow"):
    st.session_state.run_workflow = True

st.markdown("---")

# ---------------------------------------------------------
# Analyze Logic
# ---------------------------------------------------------
raw = None  # for debug display

if st.session_state.run_workflow:

    if not st.session_state.user_story.strip():
        st.error("Please enter a user story before generating.")
        st.session_state.run_workflow = False
    else:
        with st.spinner("Analyzing user story..."):
    prompt = build_prompt(st.session_state.user_story)

    # ⭐ ADD THIS DEBUG BLOCK HERE ⭐
    st.caption("🔎 Debug – final prompt sent to AI:")
    st.code(prompt, language="text")
    # ⭐ END DEBUG BLOCK ⭐

    raw = ask_ai(prompt)
            

            # DEBUG: show raw AI output
            st.caption("🔎 Debug – raw AI output:")
            st.code(raw or "<EMPTY>", language="json")

            parsed = safe_json_parse(raw)

            if parsed is None:
                st.error("The AI returned invalid JSON. Showing raw output:")
                st.code(raw)
            else:
                st.session_state.workflow_result = parsed
                st.session_state.run_workflow = False  # reset flag

# ---------------------------------------------------------
# Output Section
# ---------------------------------------------------------
result = st.session_state.workflow_result

if result:
    st.subheader("📋 Workflow Output")

    # DEBUG: show parsed JSON
    st.caption("🔎 Debug – parsed JSON object:")
    st.json(result)

    # Check if everything is empty
    all_empty = all(
        not result.get(key)
        for key in ["acceptance_criteria", "workflow_steps", "risks", "test_cases", "metrics"]
    )
    if all_empty:
        st.warning("The AI returned an empty workflow. This usually means it received an empty or unclear user story.")

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

