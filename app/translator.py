import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=GROQ_API_KEY)


def translate_news(title, description):
    prompt = f"""
تو مترجم و ویراستار اخبار فوتبالی برای یک کانال تلگرامی هستی.

عنوان و متن خبر زیر را به فارسی روان و طبیعی ترجمه کن.

قوانین:
- ترجمه خشک و کتابی نباشد.
- کمی چاشنی خودمانی و جذاب داشته باشد.
- لحن همچنان خبری و حرفه‌ای بماند.
- معنی خبر را تغییر نده.
- هیچ اطلاعات جدیدی اضافه نکن.
- خبر را خلاصه نکن.
- فقط ترجمه را برگردان.

خروجی را دقیقاً در این قالب بده:

TITLE:
عنوان فارسی

DESCRIPTION:
متن فارسی

عنوان انگلیسی:
{title}

متن انگلیسی:
{description or ""}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    if "TITLE:" not in content or "DESCRIPTION:" not in content:
        raise ValueError("Invalid translation format")

    title_fa = content.split("TITLE:", 1)[1].split("DESCRIPTION:", 1)[0].strip()
    description_fa = content.split("DESCRIPTION:", 1)[1].strip()

    return title_fa, description_fa