import feedparser
from app.database import save_news


RSS_URL = "https://www.espn.com/espn/rss/soccer/news"


def fetch_news():
    feed = feedparser.parse(RSS_URL)

    fetched = len(feed.entries)
    new_count = 0

    print(f"Fetched: {fetched}")

    for item in feed.entries:

        title = item.get("title", "").strip()
        url = item.get("link", "").strip()
        description = item.get("summary", "").strip()

        if not title or not url:
            continue

        inserted = save_news(
            title=title,
            description=description,
            url=url,
            source="ESPN"
        )

        if inserted:
            new_count += 1

    print(f"New: {new_count}")


if __name__ == "__main__":
    fetch_news()