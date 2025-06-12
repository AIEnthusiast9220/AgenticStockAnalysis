import feedparser

def fetch_news(stock):
    try:
        feed_url = f"https://news.google.com/rss/search?q={stock}+stock&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(feed_url)
        return [{"title": entry.title, "summary": entry.summary} for entry in feed.entries[:5]]
    except Exception as e:
        return []