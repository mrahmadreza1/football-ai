import psycopg2
from app.config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'news'
    ORDER BY ordinal_position
""")

for row in cur.fetchall():
    print(row[0])

cur.close()
conn.close()