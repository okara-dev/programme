#!/usr/bin/env python3
"""
Snack-Bot
- KI erfindet Mini-Snacks aus Zutaten
- TheMealDB: Rezepte
- TheCocktailDB: Cocktails
- Open Food Facts: Nährwerte
"""

import json
import sys
import os
from datetime import datetime

from llm_client import LLMClient
from apis import TheMealDBAPI, TheCocktailDBAPI, OpenFoodFactsAPI

RATING_FILE = "rating.json"

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_ratings():
    if os.path.exists(RATING_FILE):
        try:
            with open(RATING_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception as e:
            print(f"⚠️ rating.json Fehler: {e}")
    return {"snacks": []}

def save_rating(rating_data):
    with open(RATING_FILE, "w", encoding="utf-8") as f:
        json.dump(rating_data, f, indent=2, ensure_ascii=False)

def show_help():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                       🍔 SNACK-BOT                           ║
╚══════════════════════════════════════════════════════════════╝

BEFEHLE:

  🍔 REZEPTE (TheMealDB)
     "rezept pizza"
     "zufall rezept"

  🍹 COCKTAILS (TheCocktailDB)
     "cocktail mojito"
     "zufall cocktail"

  🥗 PRODUKTE (Open Food Facts)
     "produkt nutella"

  🧠 KI-SNACK (Groq)
     "snack haferflocken, banane, honig"

  📊 STATS
     "stats"

  ❓ HILFE
     "hilfe"

  👋 BEENDEN
     "exit"

╚══════════════════════════════════════════════════════════════╝
""")

def detect_intent(message):
    """Erkennt kurze Sätze"""
    msg_lower = message.lower().strip()
    
    # === BEENDEN ===
    if any(w in msg_lower for w in ["exit", "quit", "beenden", "tschüss", "tschuess"]):
        return "exit", None
    
    # === HILFE ===
    if any(w in msg_lower for w in ["hilfe", "help", "befehle"]):
        return "help", None
    
    # === STATS ===
    if any(w in msg_lower for w in ["stats", "statistik"]):
        return "stats", None
    
    # === REZEPT ===
    if "rezept" in msg_lower or "recipe" in msg_lower:
        if "zufall" in msg_lower or "zufällig" in msg_lower:
            return "random_recipe", None
        stopwords = ["rezept", "recipe", "für", "fuer", "nach", "such", "suche"]
        words = [w for w in message.split() if w.lower() not in stopwords]
        if words:
            return "recipe", " ".join(words)
        return "random_recipe", None
    
    # === COCKTAIL ===
    if "cocktail" in msg_lower:
        if "zufall" in msg_lower or "zufällig" in msg_lower:
            return "random_cocktail", None
        stopwords = ["cocktail", "für", "fuer", "nach", "such", "suche"]
        words = [w for w in message.split() if w.lower() not in stopwords]
        if words:
            return "cocktail", " ".join(words)
        return "random_cocktail", None
    
    # === PRODUKT ===
    if "produkt" in msg_lower or "nährwert" in msg_lower or "naehrwert" in msg_lower:
        stopwords = ["produkt", "nährwert", "naehrwert", "von", "für", "fuer"]
        words = [w for w in message.split() if w.lower() not in stopwords]
        if words:
            return "product", " ".join(words)
        return "product", None
    
    # === SNACK (KI) ===
    if "snack" in msg_lower:
        snack_idx = msg_lower.find("snack")
        zutaten = message[snack_idx + 5:].strip()
        if zutaten:
            return "snack", zutaten
        return "snack", None
    
    # === FALLBACK: Wenn Komma enthalten → Snack ===
    if "," in message:
        return "snack", message
    
    return "unknown", None

def generate_snack(llm, ingredients):
    """Lässt die KI einen Snack erfinden"""
    system_prompt = (
        "Du bist ein kreativer Hobby-Koch. Du erfindest Mini-Snacks "
        "aus einfachen Zutaten. Die Snacks sind essbar, schnell (max. 10 Min) "
        "und schmecken gut. Antworte auf Deutsch."
    )
    
    user_prompt = f"""Erfinde einen kreativen Mini-Snack aus:
{ingredients}

Antworte EXAKT in diesem Format:

NAME: [Kreativer Name]

ZUTATEN:
- [Zutat 1]
- [Zutat 2]

ZUBEREITUNG:
1. [Schritt 1]
2. [Schritt 2]

GESCHMACK: [Ein Satz]

TIP: [Kurzer Tipp]

Nur diese Zeilen, keine Erklärungen."""
    
    return llm.generate(system_prompt, user_prompt, max_tokens=800, temperature=0.95)

def parse_snack(response):
    if not response:
        return None
    
    snack = {"name": "Snack", "ingredients": [], "preparation": [], "taste": "", "tip": ""}
    
    try:
        if "NAME:" in response:
            snack["name"] = response.split("NAME:", 1)[1].split("\n")[0].strip()
        
        if "ZUTATEN:" in response:
            part = response.split("ZUTATEN:", 1)[1]
            if "ZUBEREITUNG:" in part:
                part = part.split("ZUBEREITUNG:", 1)[0]
            for line in part.strip().split("\n"):
                line = line.strip().lstrip("-•*").strip()
                if line:
                    snack["ingredients"].append(line)
        
        if "ZUBEREITUNG:" in response:
            part = response.split("ZUBEREITUNG:", 1)[1]
            if "GESCHMACK:" in part:
                part = part.split("GESCHMACK:", 1)[0]
            for line in part.strip().split("\n"):
                line = line.strip()
                if line:
                    if line[0].isdigit():
                        line = line.split(".", 1)[-1].strip()
                    snack["preparation"].append(line)
        
        if "GESCHMACK:" in response:
            part = response.split("GESCHMACK:", 1)[1]
            if "TIP:" in part:
                part = part.split("TIP:", 1)[0]
            snack["taste"] = part.strip()
        
        if "TIP:" in response:
            snack["tip"] = response.split("TIP:", 1)[1].strip()
    except Exception as e:
        print(f"⚠️ Parse-Fehler: {e}")
    
    return snack

def display_snack(snack):
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
    while True:
        try:
            rating = input("\n⭐ Bewerte den Snack (1-10, 's' = überspringen): ").strip()
            if rating.lower() == 's':
                return None
            rating_int = int(rating)
            if 1 <= rating_int <= 10:
                return rating_int
            print("❌ Bitte 1-10.")
        except ValueError:
            print("❌ Ungültige Eingabe.")
        except KeyboardInterrupt:
            return None

def show_statistics(ratings):
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
        
        top = sorted(rated, key=lambda x: x["rating"], reverse=True)[:3]
        print(f"\n🏆 TOP 3:")
        for i, s in enumerate(top, 1):
            print(f"   {i}. {s['name']} ({s['rating']}/10)")
    
    print("=" * 60)

def run_snack_bot():
    print("🍔 Snack-Bot 2.0 wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 60)
    print("💬 Schreib 'hilfe' für alle Befehle.")
    print("-" * 60)
    
    config = load_config()
    ratings = load_ratings()
    
    # APIs initialisieren
    llm = LLMClient(config["groq_api_key"])
    mealdb = TheMealDBAPI()
    cocktaildb = TheCocktailDBAPI()
    foodfacts = OpenFoodFactsAPI()
    
    while True:
        try:
            message = input("\n> ").strip()
            
            if not message:
                continue
            
            intent, arg = detect_intent(message)
            handled = True
            
            # === EXIT ===
            if intent == "exit":
                print("👋 Bis bald!")
                break
            
            # === HILFE ===
            elif intent == "help":
                show_help()
            
            # === STATS ===
            elif intent == "stats":
                show_statistics(ratings)
            
            # === REZEPT ===
            elif intent == "recipe":
                print(f"🍔 Suche Rezept '{arg}'...")
                meal = mealdb.search_recipe(arg)
                print(mealdb.format(meal))
            
            # === ZUFALLS-REZEPT ===
            elif intent == "random_recipe":
                print("🎲 Hole zufälliges Rezept...")
                meal = mealdb.get_random_recipe()
                print(mealdb.format(meal))
            
            # === COCKTAIL ===
            elif intent == "cocktail":
                print(f"🍹 Suche Cocktail '{arg}'...")
                drink = cocktaildb.search_cocktail(arg)
                print(cocktaildb.format(drink))
            
            # === ZUFALLS-COCKTAIL ===
            elif intent == "random_cocktail":
                print("🎲 Hole zufälligen Cocktail...")
                drink = cocktaildb.get_random_cocktail()
                print(cocktaildb.format(drink))
            
            # === PRODUKT ===
            elif intent == "product":
                if not arg:
                    print("❌ Welches Produkt?")
                    handled = False
                else:
                    print(f"🥗 Suche Produkt '{arg}'...")
                    product = foodfacts.search_product(arg)
                    print(foodfacts.format(product))
            
            # === SNACK (KI) ===
            elif intent == "snack":
                if not arg:
                    print("❌ Welche Zutaten? (z.B. 'snack haferflocken, banane, honig')")
                    handled = False
                else:
                    print("🧠 KI denkt nach...")
                    response = generate_snack(llm, arg)
                    if response:
                        snack = parse_snack(response)
                        display_snack(snack)
                        
                        rating = get_rating()
                        ratings["snacks"].append({
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "name": snack["name"],
                            "ingredients_input": arg,
                            "rating": rating
                        })
                        save_rating(ratings)
                        print(f"\n✅ Gespeichert mit Bewertung: {rating}/10" if rating else "\n✅ Gespeichert (ohne Bewertung)")
                    else:
                        print("❌ KI konnte keinen Snack generieren.")
                        handled = False
            
            # === UNBEKANNT ===
            else:
                print("❓ Unbekannter Befehl. Schreib 'hilfe' für alle Optionen.")
                handled = False
            
            # === NACH JEDER AUSGABE ===
            if handled and intent not in ["help", "exit"]:
                print("\n🍔 Viel Spaß beim Ausprobieren!")
                print("🤖 Kann ich noch was für dich tun?")
        
        except KeyboardInterrupt:
            print("\n\n👋 Bis bald!")
            break
        except Exception as e:
            print(f"❌ Fehler: {e}")

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        sys.exit(1)
    
    run_snack_bot()

if __name__ == "__main__":
    main()