import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except Exception as e:
            error_text = str(e).lower()

            # Retry only on rate limit or overload
            if "rate" in error_text or "limit" in error_text or "429" in error_text:
                wait = 2 ** attempt
                time.sleep(wait)
                continue

            # Unexpected error → return empty workflow JSON
            return EMPTY_WORKFLOW

    # All retries failed → return empty workflow JSON
    return EMPTY_WORKFLOW
