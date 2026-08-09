from app.database import get_connection


def fix_publish():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE news
        SET should_publish = TRUE
        WHERE importance_score >= 70
          AND viral_score >= 60
          AND is_published = FALSE
    """)

    updated = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    print(f"✅ Updated {updated} news")


if __name__ == "__main__":
    fix_publish()