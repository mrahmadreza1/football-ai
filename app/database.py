import psycopg2
from app.config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        ALTER TABLE news
        ADD COLUMN IF NOT EXISTS title_fa TEXT,
        ADD COLUMN IF NOT EXISTS description_fa TEXT
        """
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("✅ Database initialized successfully!")


def test_database():
    try:
        connection = get_connection()
        print("✅ Database connected successfully!")
        connection.close()

    except Exception as e:
        print("❌ Database connection failed:")
        print(e)


def save_news(
    title,
    url,
    source="ESPN",
    description=None,
    title_fa=None,
    description_fa=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO news (
            title,
            description,
            title_fa,
            description_fa,
            url,
            source
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
        RETURNING id
        """,
        (
            title,
            description,
            title_fa,
            description_fa,
            url,
            source
        )
    )

    result = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return result is not None


def get_news(limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            title_fa,
            description_fa,
            source,
            url,
            importance_score,
            viral_score,
            should_publish,
            is_published,
            created_at
        FROM news
        ORDER BY id DESC
        LIMIT %s
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def get_unprocessed_news():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, description
        FROM news
        WHERE importance_score IS NULL
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def update_news_scores(
    news_id,
    importance_score,
    viral_score,
    should_publish
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE news
        SET
            importance_score = %s,
            viral_score = %s,
            should_publish = %s
        WHERE id = %s
        """,
        (
            importance_score,
            viral_score,
            should_publish,
            news_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_news_for_publishing():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            title_fa,
            description_fa,
            url
        FROM news
        WHERE should_publish = TRUE
        AND is_published = FALSE
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def mark_news_as_published(news_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE news
        SET is_published = TRUE
        WHERE id = %s
        """,
        (news_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()