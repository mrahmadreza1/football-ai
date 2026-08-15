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

عنوان و متن خبر زیر را به فارسی ترجمه کن.

قوانین:
- ترجمه روان و طبیعی باشد.
- ترجمه کتابی و تحت‌اللفظی نباشد.
- کمی چاشنی خودمانی داشته باشد، اما همچنان حرفه‌ای و خبری باشد.
- جمله‌ها کوتاه و خوش‌خوان باشند.
- اصطلاحات فوتبالی را طبیعی ترجمه کن.
- نام بازیکنان، مربیان و تیم‌ها را درست حفظ کن.
- معنی خبر را تغییر نده.
- هیچ اطلاعاتی به خبر اضافه نکن.
- خبر را خلاصه نکن.
- فقط ترجمه را برگردان.
- هیچ توضیح اضافی ننویس.

خروجی را دقیقاً در قالب JSON زیر برگردان:

{{
    "title": "عنوان فارسی",
    "description": "متن فارسی"
}}

عنوان انگلیسی:
{title}

متن انگلیسی:
{description or ""}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    return result["title"], result["description"]