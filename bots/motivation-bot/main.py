#!/usr/bin/env python3
"""
Motivations-Bot
Schickt dir jeden Morgen einen persönlichen Brief
"""

import json
import sys
import os
from datetime import datetime

from llm_client import LLMClient
from apis import EmailSender, QuoteAPI

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_letter(llm, name):
    """Lässt die KI einen persönlichen Brief schreiben"""
    
    today = datetime.now()
    weekday = today.strftime("%A")
    date = today.strftime("%d.%m.%Y")
    
    system_prompt = (
        "Du bist ein einfühlsamer, warmer Briefschreiber. "
        "Du schreibst persönliche, ermutigende Briefe auf Deutsch. "
        "Dein Stil ist herzlich, aber nicht kitschig. "
        "Die Briefe sind 150-250 Wörter lang."
    )
    
    user_prompt = f"""Schreibe einen persönlichen Motivationsbrief an {name}.

Datum: {date} ({weekday})

Der Brief soll:
- Mit einer persönlichen Anrede beginnen
- Auf den heutigen Wochentag eingehen ({weekday})
- Eine ermutigende Botschaft enthalten
- Einen konkreten Tipp für den Tag geben
- Mit einer warmen Verabschiedung enden

Wichtig: Keine Betreffzeile, keine Überschrift – nur der Brieftext selbst.
Keine Markdown-Formatierung, nur reiner Text."""
    
    return llm.generate(system_prompt, user_prompt, max_tokens=600, temperature=0.85)

def run_motivation_bot():
    print("💌 Motivations-Bot wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 40)
    
    config = load_config()
    
    # LLM initialisieren
    llm = LLMClient(config["groq_api_key"])
    
    # APIs initialisieren
    quotes = QuoteAPI()
    email = EmailSender(config["email"])
    
    name = config.get("name", "Freund/in")
    
    # 1. Brief generieren
    print(f"✍️  Generiere Brief für {name}...")
    letter = generate_letter(llm, name)
    
    if not letter:
        print("❌ Brief konnte nicht generiert werden!")
        sys.exit(1)
    
    print(f"   ✅ Brief generiert ({len(letter)} Zeichen)")
    
    # 2. Zitat holen
    print("📜 Hole Zitat...")
    quote_data = quotes.get_quote()
    quote = quotes.format(quote_data)
    print(f"   ✅ {quote[:60]}...")
    
    # 3. E-Mail senden
    print("📧 Sende E-Mail...")
    success = email.send_motivation_letter(letter, quote)
    
    if success:
        print("✅ Motivations-Brief erfolgreich gesendet!")
    else:
        print("❌ Fehler beim Senden!")
        # Fallback: In Konsole ausgeben
        print("\n" + "=" * 60)
        print("📄 DEIN BRIEF (Konsole):")
        print("=" * 60)
        print(letter)
        print("\n" + quote)

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        sys.exit(1)
    
    run_motivation_bot()
    
    if "--no-pause" not in sys.argv:
        input("\nDrücke Enter zum Beenden...")

if __name__ == "__main__":
    main()