import traceback

from app.database import initialize_database
from app.collectors.news import fetch_news
from app.publisher import publish_news


def main():
    print("🚀 Football AI job started")

    try:
        initialize_database()

        print("📰 Fetching news...")
        fetch_news()

        print("📢 Publishing news...")
        publish_news()

        print("✅ Football AI job finished successfully")

    except Exception as e:
        print("❌ Job failed:")
        print(e)
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()