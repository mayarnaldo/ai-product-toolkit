import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

            # For other errors, stop immediately
            return '{"error": "Unexpected AI error. Please try again."}'

    # If all retries fail, return valid JSON fallback
    return '{"error": "AI overloaded. Please try again."}'
