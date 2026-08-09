import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_news(title, description=""):
    prompt = f"""
You are the editor of a professional football news channel.

Analyze this football news:

Title:
{title}

Description:
{description}

Return ONLY this format:
importance_score: NUMBER
viral_score: NUMBER
published: true OR false

Rules:
- importance_score: importance of the news from 0 to 100
- viral_score: potential audience interest from 0 to 100
- published: true only if the news is worth publishing
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content