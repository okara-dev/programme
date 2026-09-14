#!/usr/bin/env python3
"""
Snack-Erfinder
Erfindet kreative Mini-Snacks basierend auf deinen Zutaten
"""

import json
import sys
import os
from datetime import datetime

from llm_client import LLMClient

RATING_FILE = "rating.json"

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_ratings():
    """Lädt die Bewertungen aus rating.json"""
    if os.path.exists(RATING_FILE):
        try:
            with open(RATING_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception as e:
            print(f"⚠️ rating.json konnte nicht geladen werden: {e}")
    return {"snacks": []}

def save_rating(rating_data):
    """Speichert die Bewertungen in rating.json"""
    with open(RATING_FILE, "w", encoding="utf-8") as f:
        json.dump(rating_data, f, indent=2, ensure_ascii=False)

def generate_snack(llm, ingredients):
    """Lässt die KI einen kreativen Snack erfinden"""
    
    system_prompt = (
        "Du bist ein kreativer Hobby-Koch, der aus einfachen Zutaten "
        "mini Snacks erfindet. Deine Snacks sind immer essbar, schnell "
        "zubereitet (max. 10 Minuten) und schmecken gut. "
        "Du antwortest auf Deutsch und bist dabei charmant und unterhaltsam."
    )
    
    user_prompt = f"""Erfinde einen kreativen Mini-Snack aus folgenden Zutaten:
{ingredients}

Der Snack soll:
- Einfallsreich und lecker sein
- In maximal 10 Minuten zubereitet werden
- Mit den vorhandenen Zutaten machbar sein (du darfst Grundgewürze wie Salz, Pfeffer, Öl voraussetzen)
- Einen coolen Namen haben

Antworte EXAKT in diesem Format:

NAME: [Kreativer Name des Snacks]

ZUTATEN:
- [Zutat 1]
- [Zutat 2]
- ...

ZUBEREITUNG:
1. [Schritt 1]
2. [Schritt 2]
...

GESCHMACK:
[Ein Satz, wie der Snack schmeckt]

TIP:
[Ein kurzer Tipp oder eine witzige Bemerkung]

Wichtig: Keine Markdown-Formatierung mit ** oder ## – nur reiner Text."""
    
    return llm.generate(system_prompt, user_prompt, max_tokens=800, temperature=0.95)

def parse_snack(response):
    """Parst die KI-Antwort in strukturierte Daten"""
    if not response:
        return None
    
    snack = {
        "name": "Kreativer Snack",
        "ingredients": [],
        "preparation": [],
        "taste": "",
        "tip": "",
        "raw": response
    }
    
    try:
        # NAME
        if "NAME:" in response:
            name_part = response.split("NAME:", 1)[1]
            snack["name"] = name_part.split("\n")[0].strip()
        
        # ZUTATEN
        if "ZUTATEN:" in response:
            zutaten_part = response.split("ZUTATEN:", 1)[1]
            if "ZUBEREITUNG:" in zutaten_part:
                zutaten_part = zutaten_part.split("ZUBEREITUNG:", 1)[0]
            for line in zutaten_part.strip().split("\n"):
                line = line.strip().lstrip("-•*").strip()
                if line:
                    snack["ingredients"].append(line)
        
        # ZUBEREITUNG
        if "ZUBEREITUNG:" in response:
            zubereitung_part = response.split("ZUBEREITUNG:", 1)[1]
            if "GESCHMACK:" in zubereitung_part:
                zubereitung_part = zubereitung_part.split("GESCHMACK:", 1)[0]
            for line in zubereitung_part.strip().split("\n"):
                line = line.strip()
                if line:
                    # Nummerierung entfernen
                    if line[0].isdigit():
                        line = line.split(".", 1)[-1].strip()
                    snack["preparation"].append(line)
        
        # GESCHMACK
        if "GESCHMACK:" in response:
            geschmack_part = response.split("GESCHMACK:", 1)[1]
            if "TIP:" in geschmack_part:
                geschmack_part = geschmack_part.split("TIP:", 1)[0]
            snack["taste"] = geschmack_part.strip()
        
        # TIP
        if "TIP:" in response:
            snack["tip"] = response.split("TIP:", 1)[1].strip()
    
    except Exception as e:
        print(f"⚠️ Parsing-Fehler: {e}")
    
    return snack

def display_snack(snack):
    """Zeigt den Snack schön formatiert an"""
    print("\n" + "=" * 60)
    print(f"🍽️  {snack['name'].upper()}")
    print("=" * 60)
    
    if snack["ingredients"]:
        print("\n📋 ZUTATEN:")
        for ing in snack["ingredients"]:
            print(f"   • {ing}")
    
    if snack["preparation"]:
        print("\n👨‍🍳 ZUBEREITUNG:")
        for i, step in enumerate(snack["preparation"], 1):
            print(f"   {i}. {step}")
    
    if snack["taste"]:
        print(f"\n😋 GESCHMACK:\n   {snack['taste']}")
    
    if snack["tip"]:
        print(f"\n💡 TIPP:\n   {snack['tip']}")
    
    print("\n" + "=" * 60)

def get_rating():
    """Fragt den Nutzer nach einer Bewertung"""
    while True:
        try:
            rating = input("\n⭐ Bewerte den Snack (1-10, oder 's' zum Überspringen): ").strip()
            
            if rating.lower() == 's':
                return None
            
            rating_int = int(rating)
            if 1 <= rating_int <= 10:
                return rating_int
            else:
                print("❌ Bitte eine Zahl zwischen 1 und 10 eingeben.")
        except ValueError:
            print("❌ Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 10.")
        except KeyboardInterrupt:
            print("\n👋 Abgebrochen.")
            sys.exit(0)

def show_statistics(ratings):
    """Zeigt Statistiken über bisherige Snacks"""
    snacks = ratings.get("snacks", [])
    
    if not snacks:
        print("\n📊 Noch keine Snacks bewertet.")
        return
    
    print("\n" + "=" * 60)
    print("📊 DEINE SNACK-STATISTIK")
    print("=" * 60)
    print(f"\n🍽️  Insgesamt: {len(snacks)} Snacks")
    
    rated = [s for s in snacks if s.get("rating")]
    if rated:
        avg = sum(s["rating"] for s in rated) / len(rated)
        print(f"⭐ Durchschnitt: {avg:.1f}/10")
        
        # Top 3
        top = sorted(rated, key=lambda x: x["rating"], reverse=True)[:3]
        print(f"\n🏆 TOP 3:")
        for i, s in enumerate(top, 1):
            print(f"   {i}. {s['name']} ({s['rating']}/10)")
        
        # Letzte 5
        print(f"\n📅 LETZTE 5 SNACKS:")
        for s in snacks[-5:]:
            rating = s.get("rating", "–")
            date = s.get("date", "–")
            print(f"   • {s['name']} | {rating}/10 | {date}")
    
    print("=" * 60)

def run_snack_bot():
    print("🍳 Snack-Erfinder wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 60)
    
    config = load_config()
    ratings = load_ratings()
    
    # Statistiken anzeigen
    show_statistics(ratings)
    
    # Zutaten abfragen
    print("\n🥕 Welche Zutaten hast du da?")
    print("   (z.B. 'Haferflocken, Banane, Honig, Nüsse')")
    print("   oder 'stats' für Statistiken, 'exit' zum Beenden")
    
    ingredients = input("\n> ").strip()
    
    if ingredients.lower() in ['exit', 'quit']:
        print("👋 Bis bald!")
        return
    
    if ingredients.lower() == 'stats':
        show_statistics(ratings)
        return
    
    if not ingredients:
        print("❌ Keine Zutaten eingegeben.")
        return
    
    # LLM initialisieren
    llm = LLMClient(config["groq_api_key"])
    
    # Snack generieren
    print("\n🧠 KI denkt nach...")
    response = generate_snack(llm, ingredients)
    
    if not response:
        print("❌ Snack konnte nicht generiert werden!")
        return
    
    snack = parse_snack(response)
    
    if not snack:
        print("❌ Snack konnte nicht geparst werden!")
        return
    
    # Snack anzeigen
    display_snack(snack)
    
    # Bewertung abfragen
    rating = get_rating()
    
    # Snack mit Bewertung speichern
    snack_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": snack["name"],
        "ingredients_input": ingredients,
        "ingredients": snack["ingredients"],
        "preparation": snack["preparation"],
        "taste": snack["taste"],
        "tip": snack["tip"],
        "rating": rating
    }
    
    ratings["snacks"].append(snack_entry)
    save_rating(ratings)
    
    if rating:
        print(f"\n✅ Gespeichert mit Bewertung: {rating}/10")
    else:
        print("\n✅ Gespeichert (ohne Bewertung)")
    
    print(f"📁 Datei: {os.path.abspath(RATING_FILE)}")

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        sys.exit(1)
    
    try:
        run_snack_bot()
    except KeyboardInterrupt:
        print("\n\n👋 Bis bald!")

if __name__ == "__main__":
    main()