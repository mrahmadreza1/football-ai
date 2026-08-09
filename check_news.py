from app.database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT
        id,
        title,
        importance_score,
        viral_score,
        should_publish,
        is_published
    FROM news
    ORDER BY id DESC
    LIMIT 20
""")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()