"""
Wikipedia API – holt Artikel-Zusammenfassungen
Nutzt die REST API (wie die PowerShell-Funktion 'r')
"""

import requests
from urllib.parse import quote

class WikipediaAPI:
    def __init__(self, sprache="de"):
        self.base_url = f"https://{sprache}.wikipedia.org/api/rest_v1"
        self.sprache = sprache
        # User-Agent trotzdem setzen (sicherer)
        self.headers = {
            "User-Agent": "LernBot/1.0 (https://github.com/okara-dev)"
        }
    
    def get_summary(self, title):
        """Holt die Zusammenfassung eines Artikels über die REST API"""
        # URL-Encoding für Sonderzeichen
        encoded_title = quote(title)
        url = f"{self.base_url}/page/summary/{encoded_title}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "title": data.get("title", title),
                "extract": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "thumbnail": data.get("thumbnail", {}).get("source", "")
            }
        except Exception as e:
            print(f"⚠️ Wikipedia Summary Fehler: {e}")
            return None
    
    def get_random_article(self):
        """Holt einen zufälligen Wikipedia-Artikel"""
        url = f"{self.base_url}/page/random/summary"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "title": data.get("title", ""),
                "extract": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "thumbnail": data.get("thumbnail", {}).get("source", "")
            }
        except Exception as e:
            print(f"⚠️ Wikipedia Random Fehler: {e}")
            return None
    
    def get_by_topic(self, thema, unterthema):
        """Sucht nach einem Artikel zum Unterthema über die REST API"""
        # Versuche zuerst den Suchbegriff direkt
        result = self.get_summary(unterthema)
        
        if result and result.get("extract"):
            return result
        
        # Falls nicht gefunden, versuche mit Thema
        result = self.get_summary(f"{unterthema} ({thema})")
        
        if result and result.get("extract"):
            return result
        
        # Fallback: Zufälliger Artikel
        print("   ⚠️ Kein Artikel gefunden, verwende zufälligen Artikel")
        return self.get_random_article()