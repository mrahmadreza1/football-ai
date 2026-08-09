from app.database import get_connection


def migrate_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        ALTER TABLE news
        ADD COLUMN IF NOT EXISTS should_publish BOOLEAN DEFAULT FALSE;
    """)

    cursor.execute("""
        ALTER TABLE news
        ADD COLUMN IF NOT EXISTS is_published BOOLEAN DEFAULT FALSE;
    """)

    cursor.execute("""
        UPDATE news
        SET should_publish =
            CASE
                WHEN importance_score >= 70
                AND viral_score >= 60
                THEN TRUE
                ELSE FALSE
            END;
    """)

    connection.commit()

    cursor.close()
    connection.close()

    print("✅ Database migration completed!")


if __name__ == "__main__":
    migrate_database()