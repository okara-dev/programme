"""
RSS-News aus verschiedenen Quellen
"""

import feedparser
from datetime import datetime
from .translator import translate_text

class RSSNews:
    def __init__(self):
        # Verschiedene RSS-Feeds
        self.feeds = [
            "https://www.tagesschau.de/index~rss2.xml",
            "https://www.spiegel.de/schlagzeilen/tops/index.rss"
        ]
    
    def get_headlines(self, max_articles=5):
        """Holt die neuesten Schlagzeilen aus allen Feeds"""
        all_articles = []
        
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:  # 3 pro Feed
                    all_articles.append({
                        "title": entry.get("title", "Kein Titel"),
                        "link": entry.get("link", "#"),
                        "source": feed.feed.get("title", "Unbekannt"),
                        "published": entry.get("published", "Kein Datum")
                    })
            except Exception as e:
                print(f"⚠️ RSS-Feed Fehler ({feed_url}): {e}")
        
        # Sortieren nach Datum (neueste zuerst)
        all_articles = all_articles[:max_articles]
        return all_articles
    
    def format(self, articles):
        if not articles:
            return "📰 Keine News verfügbar."
        
        lines = ["📰 **TOP-NACHRICHTEN**", "=" * 35]
        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "Kein Titel")
            source = article.get("source", "Unbekannt")
            link = article.get("link", "#")
            
            lines.append(f"{i}. **{title}**")
            lines.append(f"   📌 {source} | [Link]({link})")
            lines.append("")
        
        return "\n".join(lines)