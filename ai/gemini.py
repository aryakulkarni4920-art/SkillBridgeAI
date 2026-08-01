import os
import time

from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(career, resume_text):

    prompt = f"""
You are an expert AI Career Coach.

Analyze this resume according to the user's career goal.

Career Goal:
{career}

Resume Content:
{resume_text}

Return ONLY valid JSON.

Do not use markdown.
Do not write explanations.
Do not use ```json.

Return exactly this structure:

{{
    "match_score": 0,
    "existing_skills": [],
    "missing_skills": [],
    "roadmap": [],
    "courses": []
}}

Rules:

1. match_score must be a number between 0 and 100.
2. existing_skills should contain skills already present.
3. missing_skills should contain skills needed for the career goal.
4. roadmap should contain practical learning steps.
5. courses should return ONLY course names.

Example:

[
"Python for Everybody",
"SQL for Data Science",
"Docker for Beginners"
]

Do NOT include URLs.
Do NOT include descriptions.
Return only course titles.
6. Keep the answer concise.
"""

    try:

        # Retry up to 3 times if Gemini is busy
        for i in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt,
                )

                return response.text

            except Exception as e:

                if i < 2:
                    print(f"Gemini busy... Retrying ({i+1}/3)")
                    time.sleep(5)
                else:
                    raise e

    except Exception as e:

        print("\n========== GEMINI ERROR ==========\n")
        print(type(e))
        print(str(e))
        print("\n==================================\n")

        raise e