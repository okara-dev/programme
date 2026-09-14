#!/usr/bin/env python3
"""
Story-Bot
Schickt dir jeden Tag eine neue Kurzgeschichte
"""

import json
import sys
import os
import random
from datetime import datetime

from llm_client import LLMClient
from apis import EmailSender

# Themen-Pool für Abwechslung
STORY_THEMES = [
    "ein einsamer Leuchtturmwärter, der eines Tages Besuch bekommt",
    "ein Kind, das eine magische Feder findet",
    "eine Bibliothekarin, die ein Buch entdeckt, das noch nicht geschrieben wurde",
    "ein alter Uhrmacher, der die Zeit anhalten kann",
    "ein Pilot, der auf einer unbekannten Insel notlandet",
    "eine Katze, die die Sprache der Menschen versteht",
    "ein Wanderer, der einen sprechenden Baum trifft",
    "eine Köchin, die mit ihren Gerichten Erinnerungen wecken kann",
    "ein Astronaut, der auf einem verlassenen Planeten ein Zeichen findet",
    "ein Musiker, der mit seiner Melodie Herzen heilen kann",
    "ein Kind, das mit seinem Schatten befreundet ist",
    "eine Malerin, deren Bilder Wirklichkeit werden",
]

GENRES = [
    "magischer Realismus",
    "Abenteuer",
    "Science-Fiction",
    "Märchen für Erwachsene",
    "Poetisch-philosophisch",
    "Fantasy",
]

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_story(llm, theme, genre, temperature=0.9):
    """Lässt die KI eine Geschichte schreiben"""
    
    system_prompt = (
        "Du bist ein begabter deutschsprachiger Schriftsteller. "
        "Du schreibst kurze, fesselnde Geschichten mit Tiefgang. "
        "Dein Stil ist bildhaft, atmosphärisch und poetisch, aber nicht überladen. "
        "Du beherrschst die Kunst der kurzen Erzählung."
    )
    
    user_prompt = f"""Schreibe eine kurze Geschichte (ca. 400-500 Wörter).

Thema: {theme}
Genre: {genre}

Die Geschichte soll:
- Einen packenden Einstieg haben
- Lebendige Charaktere und Atmosphäre erschaffen
- Einen Wendepunkt oder eine überraschende Erkenntnis enthalten
- Mit einer tiefgründigen Moral oder Botschaft enden

Antworte EXAKT in diesem Format:

TITEL: [Ein kurzer, poetischer Titel]

GESCHICHTE:
[Der vollständige Text der Geschichte]

MORAL:
[Ein Satz, der die Kernbotschaft zusammenfasst]

Wichtig: Keine Markdown-Formatierung, nur reiner Text."""
    
    response = llm.generate(system_prompt, user_prompt, max_tokens=1500, temperature=temperature)
    
    if not response:
        return None
    
    # Antwort parsen
    title = "Eine Geschichte"
    story = response
    moral = "Jede Geschichte trägt eine Wahrheit in sich."
    
    try:
        if "TITEL:" in response:
            parts = response.split("TITEL:", 1)[1]
            if "GESCHICHTE:" in parts:
                title = parts.split("GESCHICHTE:", 1)[0].strip()
                story = parts.split("GESCHICHTE:", 1)[1]
                
                if "MORAL:" in story:
                    moral = story.split("MORAL:", 1)[1].strip()
                    story = story.split("MORAL:", 1)[0].strip()
    except Exception as e:
        print(f"⚠️ Parsing-Fehler: {e}")
    
    return {
        "title": title,
        "story": story.strip(),
        "moral": moral,
        "genre": genre,
        "theme": theme
    }

def run_story_bot():
    print("📖 Story-Bot wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 40)
    
    config = load_config()
    
    # LLM initialisieren
    llm = LLMClient(config["groq_api_key"])
    
    # E-Mail initialisieren
    email = EmailSender(config["email"])
    
    # Zufälliges Thema und Genre wählen
    theme = random.choice(STORY_THEMES)
    genre = random.choice(GENRES)
    
    print(f"🎭 Genre: {genre}")
    print(f"📌 Thema: {theme[:60]}...")
    print()
    
    # Geschichte generieren
    print("✍️  Generiere Geschichte...")
    story_data = generate_story(llm, theme, genre, temperature=0.9)
    
    if not story_data:
        print("❌ Geschichte konnte nicht generiert werden!")
        sys.exit(1)
    
    print(f"   ✅ Titel: {story_data['title']}")
    print(f"   ✅ {len(story_data['story'])} Zeichen")
    print(f"   ✅ Moral: {story_data['moral'][:60]}...")
    
    # E-Mail senden
    print("\n📧 Sende E-Mail...")
    success = email.send_story(
        story_data["title"],
        story_data["story"],
        story_data["genre"],
        story_data["moral"]
    )
    
    if success:
        print("✅ Geschichte erfolgreich gesendet!")
    else:
        print("❌ Fehler beim Senden!")
        # Fallback: In Konsole ausgeben
        print("\n" + "=" * 60)
        print(f"📖 {story_data['title']}")
        print("=" * 60)
        print(story_data["story"])
        print("\n💡 Moral: " + story_data["moral"])

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        sys.exit(1)
    
    run_story_bot()
    
    if "--no-pause" not in sys.argv:
        input("\nDrücke Enter zum Beenden...")

if __name__ == "__main__":
    main()