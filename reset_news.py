from app.database import get_connection


def reset_news():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM news;")

    connection.commit()

    cursor.close()
    connection.close()

    print("✅ All news data deleted!")


if __name__ == "__main__":
    reset_news()