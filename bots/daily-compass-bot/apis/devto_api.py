"""
Dev.to API – Tech-Artikel von der Entwickler-Community
Kostenlos, kein API-Key nötig
"""

import requests

class DevToAPI:
    def __init__(self):
        self.base_url = "https://dev.to/api"
    
    def get_top_articles(self, limit=5, tag=None):
        """Holt die Top-Artikel von Dev.to"""
        try:
            params = {"per_page": limit, "top": 1}
            if tag:
                params["tag"] = tag
            
            response = requests.get(
                f"{self.base_url}/articles",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ Dev.to Fehler: {e}")
            return []
    
    def format(self, articles):
        if not articles:
            return "👨‍💻 Keine Dev.to-Artikel verfügbar."
        
        lines = ["👨‍💻 **DEV.TO – TECH-ARTIKEL**", "=" * 35]
        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "Kein Titel")
            url = article.get("url", "#")
            author = article.get("user", {}).get("name", "Unbekannt")
            reactions = article.get("positive_reactions_count", 0)
            
            lines.append(f"{i}. **{title}**")
            lines.append(f"   ✍️ {author} | ❤️ {reactions} | [Link]({url})")
            lines.append("")
        
        return "\n".join(lines)