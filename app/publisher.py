import os
import requests

from dotenv import load_dotenv

from app.database import (
    get_news_for_publishing,
    mark_news_as_published
)


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_LINK = "https://t.me/FotballPersian"

def send_photo(photo_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL_ID,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    response.raise_for_status()


def send_video(video_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    response = requests.post(
        url,
        json={
            "chat_id": CHANNEL_ID,
            "video": video_url,
            "caption": caption,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    response.raise_for_status()


def send_text(text):
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


def publish_news():
    news_list = get_news_for_publishing()

    print(f"Found {len(news_list)} news for publishing")

    for (
        news_id,
        title,
        description,
        title_fa,
        description_fa,
        url,
        image_url,
        video_url
    ) in news_list:

        try:
            # استفاده از ترجمه ذخیره‌شده در دیتابیس
            title_fa = title_fa or title
            description_fa = description_fa or description or ""

            # ساخت متن نهایی برای تلگرام
            caption = (
                f"⚽🔥 <b>{title_fa}</b>\n\n"
                f"{description_fa}\n\n"
                f"🔗 <a href=\"{url}\">منبع خبر</a>\n"
                f"📢 <a href=\"{CHANNEL_LINK}\">کانال فوتبال پرشین</a>"
            )
            

            # ارسال به تلگرام
            if video_url:
                send_video(video_url, caption)

            elif image_url:
                send_photo(image_url, caption)

            else:
                send_text(caption)

            # علامت‌گذاری به عنوان منتشرشده
            mark_news_as_published(news_id)

            print(f"✅ Published: {title}")

        except Exception as e:
            print(f"❌ Failed: {title}")
            print(e)


if __name__ == "__main__":
    publish_news()