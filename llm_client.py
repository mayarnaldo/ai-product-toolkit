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
            # Handle rate limits or temporary overload
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                # For other errors, raise immediately
                raise e

    # If all retries fail
    return "The AI is currently overloaded. Please try again in a moment."
