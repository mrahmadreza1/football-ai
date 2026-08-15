import os
import requests

from dotenv import load_dotenv

from app.database import (
    get_news_for_publishing,
    mark_news_as_published
)

from app.translator import translate_news


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise Exception(data)

    return True


def publish_news():
    news_list = get_news_for_publishing()

    print(f"Found {len(news_list)} news for publishing")

    for news_id, title, description, url in news_list:

        try:
            # ترجمه عنوان و توضیحات با یک درخواست API
            title_fa, description_fa = translate_news(
                title,
                description
            )

            # ساخت متن نهایی برای تلگرام
            text = (
                f"<b>{title_fa}</b>\n\n"
                f"{description_fa}\n\n"
                f"🔗 <a href=\"{url}\">منبع خبر</a>"
            )

            # ارسال به کانال
            send_to_telegram(text)

            # علامت‌گذاری خبر به عنوان منتشرشده
            mark_news_as_published(news_id)

            print(f"✅ Published: {title}")

        except Exception as e:
            print(f"❌ Failed: {title}")
            print(e)


if __name__ == "__main__":
    publish_news()