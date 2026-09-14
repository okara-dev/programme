#!/usr/bin/env python3
"""
Daily Compass – Dein täglicher Begleiter mit News, NASA, Sprichwörtern & Witz
"""

import json
import sys
import os
from datetime import datetime

from apis.rss_news import RSSNews
from apis.nasa_api import NASAAPI
from apis.proverbs_api import ProverbsAPI
from apis.joke_api import JokeAPI
from apis.email_sender import EmailSender

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def run_compass():
    print("🧭 Daily Compass wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 40)
    
    config = load_config()
    keys = config["api_keys"]
    
    # APIs initialisieren
    news = RSSNews()
    nasa = NASAAPI(keys["nasa_api"])
    proverbs = ProverbsAPI()
    joke = JokeAPI()
    email = EmailSender(config["email"])
    
    print("📡 Rufe Daten von APIs ab...")
    
    # 1. News
    print("  📰 News (RSS)...")
    articles = news.get_headlines(max_articles=5)
    news_content = news.format(articles)
    
    # 2. NASA
    print("  🚀 NASA...")
    nasa_data = nasa.get_apod()
    if nasa_data:
        nasa_content = nasa.format(nasa_data)
    else:
        nasa_content = "🚀 NASA-Bild nicht verfügbar"
    
    # 3. Sprichwort
    print("  📜 Sprichwort...")
    proverb_data = proverbs.get_proverb()
    proverb_content = proverbs.format(proverb_data) if proverb_data else "📜 Kein Sprichwort verfügbar"
    
    # 4. Witz
    print("  😂 Witz...")
    joke_data = joke.get_joke()
    joke_content = joke.format(joke_data) if joke_data else "😂 Kein Witz verfügbar"
    
    # E-Mail senden
    print("\n📧 Sende E-Mail...")
    success = email.send_daily_compass(
        news_content, nasa_content,
        proverb_content, joke_content
    )
    
    if success:
        print("✅ Daily Compass erfolgreich gesendet!")
    else:
        print("❌ Fehler beim Senden!")

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        print("   Erstelle eine config.json mit deinen Einstellungen.")
        sys.exit(1)
    
    run_compass()
    
    if "--no-pause" not in sys.argv:
        input("\nDrücke Enter zum Beenden...")

if __name__ == "__main__":
    main()