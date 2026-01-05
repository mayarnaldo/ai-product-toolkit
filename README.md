🧠 AI Product Toolkit
A multi‑assistant Streamlit app that transforms user stories, feature ideas, and stakeholder notes into structured product artifacts.
🚀 Features
🧩 Story‑to‑Workflow Assistant
Converts user stories into:
- Acceptance criteria
- Workflow steps
- Risks & dependencies
- Test cases
- Success metrics
- 
📌 Feature Prioritization Assistant
Ranks features using:
- RICE
- MoSCoW
- Value vs Effort
- AI‑guided logic
Outputs include reasoning and clarifying questions.

🤝 Stakeholder Alignment Assistant
Turns stakeholder notes into:
- Areas of agreement
- Misalignment
- Suggested compromises
- A meeting‑ready narrative
- 
🛠️ Tech Stack
- Python
- Streamlit
- OpenAI API
- python‑dotenv

- 
📁 Project Structure
ai-product-toolkit/
│
├── Home.py
├── prompts.py
├── llm_client.py
├── requirements.txt
└── pages/
    ├── 1_Story_to_Workflow_Assistant.py
    ├── 2_Feature_Prioritization_Assistant.py
    └── 3_Stakeholder_Alignment_Assistant.py
Running Locally
pip install -r requirements.txt
streamlit run Home.py

🌐 Deployment
Compatible with Streamlit Cloud.
Set Main file = Home.py and add your OPENAI_API_KEY in Secrets.
⏳ Note: The live demo may take a few seconds to wake up if inactive.


🎯 Why This Project Matters
This toolkit demonstrates:
- Hands‑on AI product development
- Prompt engineering
- Multi‑page Streamlit UI design
- Real product workflows
- PM‑ready communication and structure

📬 Contact
Built by May Urania A. Arnaldo
Product Owner → Product Manager
