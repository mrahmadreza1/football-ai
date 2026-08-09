from app.database import get_unprocessed_news, update_news_scores
from app.ai_editor import analyze_news


def process_news():
    news_list = get_unprocessed_news()

    print(f"Found {len(news_list)} unprocessed news")

    for news_id, title, description in news_list:

        print(f"\n📰 Analyzing: {title}")

        try:
            result = analyze_news(
                title,
                description or ""
            )

            print(result)

            importance = None
            viral = None

            for line in result.splitlines():
                line = line.strip()

                if line.startswith("importance_score:"):
                    importance = int(
                        line.split(":", 1)[1].strip()
                    )

                elif line.startswith("viral_score:"):
                    viral = int(
                        line.split(":", 1)[1].strip()
                    )

            if importance is None or viral is None:
                print("⚠️ Invalid AI response")
                continue

            # قانون انتشار
            should_publish = (
                importance >= 70
                and viral >= 60
            )

            update_news_scores(
                news_id,
                importance,
                viral,
                should_publish
            )

            print(
                f"✅ Saved | "
                f"Importance: {importance} | "
                f"Viral: {viral} | "
                f"Publish: {should_publish}"
            )

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    process_news()