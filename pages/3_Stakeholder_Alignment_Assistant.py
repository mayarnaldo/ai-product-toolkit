import streamlit as st
import json
from llm_client import ask_ai
from prompts import build_alignment_prompt

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("🤝 Stakeholder Alignment Assistant")

# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------
st.title("🤝 Stakeholder Alignment Assistant")
st.caption("Turn scattered notes into clarity, alignment, and shared direction.")

st.markdown("---")

# ---------------------------------------------------------
# Session State Setup
# ---------------------------------------------------------
if "stakeholders" not in st.session_state:
    st.session_state.stakeholders = ["Stakeholder 1"]

if "alignment_result" not in st.session_state:
    st.session_state.alignment_result = None

# ---------------------------------------------------------
# Stakeholder Inputs Section
# ---------------------------------------------------------
st.subheader("📝 Stakeholder Inputs")

# Render text areas for each stakeholder
notes_dict = {}
for idx, name in enumerate(st.session_state.stakeholders):
    notes = st.text_area(f"Paste notes from {name}", key=f"notes_{idx}")
    notes_dict[name] = notes

# Add stakeholder button
if st.button("➕ Add Another Stakeholder"):
    new_number = len(st.session_state.stakeholders) + 1
    st.session_state.stakeholders.append(f"Stakeholder {new_number}")
    st.rerun()

# Analyze button
analyze_clicked = st.button("🔍 Analyze Alignment")

st.markdown("---")

# ---------------------------------------------------------
# Analyze Logic
# ---------------------------------------------------------
if analyze_clicked:
    # Combine notes into a single block
    combined_notes = "\n\n".join(
        [f"{name}:\n{notes}" for name, notes in notes_dict.items() if notes.strip()]
    )

    if not combined_notes.strip():
        st.error("Please enter at least one stakeholder's notes before analyzing.")
    else:
        with st.spinner("Analyzing stakeholder alignment..."):
            prompt = build_alignment_prompt(combined_notes)
            raw = ask_ai(prompt)

            try:
                data = json.loads(raw)
                st.session_state.alignment_result = data
            except:
                st.error("The AI returned invalid JSON. Showing raw output:")
                st.code(raw)

# ---------------------------------------------------------
# Alignment Insights Section
# ---------------------------------------------------------
if st.session_state.alignment_result:
    result = st.session_state.alignment_result

    st.subheader("🤝 Alignment Insights")

    # Areas of Agreement
    st.markdown("### ✅ Areas of Agreement")
    for item in result.get("agreement", []):
        st.markdown(f"- {item}")

    # Conflicts & Misalignment
    st.markdown("### ⚠️ Conflicts & Misalignment")
    for item in result.get("misalignment", []):
        st.markdown(f"- {item}")

    st.markdown("---")

    # ---------------------------------------------------------
    # Suggested Compromise & Narrative
    # ---------------------------------------------------------
    st.subheader("🧩 Suggested Compromise & Narrative")

    st.markdown("### 🤝 Suggested Compromise")
    st.markdown(result.get("compromise", ""))

    st.markdown("### 📝 Alignment Narrative")
    st.markdown(result.get("narrative", ""))

    # Copy button
    st.button("📋 Copy Alignment Summary")

else:
    st.info("No analysis yet. Add stakeholder notes and click **Analyze Alignment**.")
    