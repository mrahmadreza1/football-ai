import psycopg2
from app.config import DATABASE_URL


def create_tables():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            source TEXT,
            url TEXT UNIQUE,
            category VARCHAR(50),
            importance_score INTEGER,
            viral_score INTEGER,
            published BOOLEAN DEFAULT FALSE,
            video_available BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    connection.commit()
    cursor.close()
    connection.close()

    print("✅ News table created successfully!")


if __name__ == "__main__":
    create_tables()