from app.database import get_news

news = get_news()

for item in news:
    print(item)