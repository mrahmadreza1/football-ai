import os
from dotenv import load_dotenv
from telegram import Bot
from app.database import get_connection

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def get_approved_news():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, description, url
        FROM news
        WHERE published = TRUE
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def mark_as_published(news_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE news
        SET published = FALSE
        WHERE id = %s
    """, (news_id,))

    connection.commit()
    cursor.close()
    connection.close()


def publish_news():
    bot = Bot(token=BOT_TOKEN)
    news_list = get_approved_news()

    print(f"Found {len(news_list)} approved news")

    for news_id, title, description, url in news_list:

        message = f"""
⚽ <b>{title}</b>

{description or ""}

🔗 <a href="{url}">منبع خبر</a>
"""

        bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode="HTML"
        )

        mark_as_published(news_id)

        print(f"✅ Published: {title}")


if __name__ == "__main__":
    publish_news()