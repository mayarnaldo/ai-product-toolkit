import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fallback JSON that matches your UI structure
EMPTY_WORKFLOW = """
{
  "acceptance_criteria": [],
  "workflow_steps": [],
  "risks": [],
  "test_cases": [],
  "metrics": []
}
"""

def ask_ai(prompt, max_retries=5):
    """
    Calls the OpenAI API with retry logic.
    Always returns valid JSON so Streamlit never breaks.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",   # More stable than gpt-4o-mini
                messages=[{"role": "user", "content": prompt}]
            )

            raw = response.choices[0].message.content

            # If model returns empty or None → fallback
            if not raw or raw.strip() == "":
                return EMPTY_WORKFLOW

            return raw

        except Exception as e:
            error_text = str(e).lower()

            # Retry only on rate limit or overload
            if "rate" in error_text or "limit" in error_text or "429" in error_text:
                wait = 2 ** attempt
                time.sleep(wait)
                continue

            # Unexpected error → return safe JSON
            return EMPTY_WORKFLOW

    # All retries failed → return safe JSON
    return EMPTY_WORKFLOW
