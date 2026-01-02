import streamlit as st
st.set_page_config(page_title="Home", page_icon="🏠")
# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("🏠 Home")
st.sidebar.markdown("Welcome to your AI Product Toolkit.")

# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------
st.title("🧠 AI Product Toolkit")
st.caption("A suite of AI-powered assistants for Product Owners and Product Managers.")

st.markdown("---")

# ---------------------------------------------------------
# Intro Section
# ---------------------------------------------------------
st.subheader("✨ Welcome")

st.write(
    """
This toolkit brings together three powerful AI assistants designed to help you move 
from ambiguity to clarity — faster and with more confidence.

Whether you're refining user stories, prioritizing features, or aligning stakeholders, 
each assistant is built to support real product workflows.
"""
)

st.markdown("---")

# ---------------------------------------------------------
# Assistant Overview
# ---------------------------------------------------------
st.subheader("🧰 Available Assistants")

st.markdown("### 🧩 Story-to-Workflow Assistant")
st.write(
    """
Convert user stories into structured product artifacts — acceptance criteria, workflows, risks, test cases, and metrics.
"""
)


st.link_button("Open Story-to-Workflow Assistant", "/Story_to_Workflow_Assistant")

st.markdown("---")

st.markdown("### 📌 Feature Prioritization Assistant")
st.write(
    """
Analyze feature ideas using RICE, MoSCoW, Value vs Effort, or a custom AI-guided framework. 
Get ranked features and clear explanations.
"""
)
st.link_button("Open Feature Prioritization Assistant", "/Feature_Prioritization_Assistant")

st.markdown("---")

st.markdown("### 🤝 Stakeholder Alignment Assistant")
st.write(
    """
Turn scattered stakeholder notes into alignment insights, conflict summaries, 
compromise suggestions, and a meeting-ready narrative.
"""
)
st.link_button("Open Stakeholder Alignment Assistant", "/Stakeholder_Alignment_Assistant")

st.markdown("---")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.caption("Built by May Arnaldo• Product Owner & AI Builder")