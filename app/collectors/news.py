import feedparser

from app.database import save_news, initialize_database
from app.translator import translate_news


RSS_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml"


def fetch_news():
    initialize_database()
    feed = feedparser.parse(RSS_URL)

    print(feed.bozo)
    print(feed.bozo_exception if feed.bozo else "RSS OK")
    print(feed.get("status"))

    fetched = len(feed.entries)
    new_count = 0

    print(f"Fetched: {fetched}")

    for item in feed.entries:

        title = item.get("title", "").strip()
        url = item.get("link", "").strip()
        description = item.get("summary", "").strip()
        image_url=""
        if "media_content" in item:
            image_url = item.media_content[0].get("url", "")

        elif "media_thumbnail" in item:
            image_url = item.media_thumbnail[0].get("url", "")

        if not title or not url:
            continue

        try:
            # ترجمه عنوان و توضیحات با یک درخواست Groq
            title_fa, description_fa = translate_news(
                title,
                description
            )

            # ذخیره خبر انگلیسی + فارسی
            inserted = save_news(
                title=title,
                description=description,
                title_fa=title_fa,
                description_fa=description_fa,
                url=url,
                source="BBC",
                image_url=image_url,
                video_url=None
            )

            if inserted:
                new_count += 1
                print(f"✅ Saved: {title}")

        except Exception as e:
            print(f"❌ Failed: {title}")
            print(e)

    print(f"New: {new_count}")


if __name__ == "__main__":
    fetch_news()