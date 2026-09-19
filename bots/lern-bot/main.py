#!/usr/bin/env python3
"""
Lern-Bot
Tägliches Lernthema aus Physik, Biologie oder Psychologie
"""

import json
import sys
import os
import random
from datetime import datetime

from llm_client import LLMClient
from apis import WikipediaAPI, EmailSender

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_lernthema(llm, kategorie):
    """Lässt die KI ein interessantes Unterthema wählen und erklären"""
    
    system_prompt = (
        f"Du bist ein begeisterter {kategorie}-Lehrer. "
        "Du erklärst komplexe Themen einfach, verständlich und spannend auf Deutsch. "
        "Du weckst Neugier und Freude am Lernen."
    )
    
    user_prompt = f"""Wähle ein interessantes Unterthema aus dem Bereich {kategorie}.

Es soll:
- Für einen neugierigen Erwachsenen spannend sein
- Nicht zu speziell, aber auch nicht zu oberflächlich
- Alltagsbezug haben, wenn möglich
- In 3-4 Absätzen erklärbar sein

Antworte EXAKT in diesem Format:

THEMA: [Name des Unterthemas]

ERKLAERUNG:
[3-4 Absätze einfache Erklärung auf Deutsch]

WIKIPEDIA_SUCHBEGRIFF: [Der beste Suchbegriff für Wikipedia]

FUN_FACT: [Ein überraschender Fakt zum Thema]

Nur diese Zeilen, keine zusätzlichen Erklärungen."""
    
    response = llm.generate(system_prompt, user_prompt, max_tokens=1500, temperature=0.8)
    
    if not response:
        return None
    
    data = {
        "thema": "Unbekanntes Thema",
        "erklaerung": "",
        "suchbegriff": kategorie,
        "fun_fact": ""
    }
    
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("THEMA:"):
            data["thema"] = line.replace("THEMA:", "").strip()
        elif line.startswith("WIKIPEDIA_SUCHBEGRIFF:"):
            data["suchbegriff"] = line.replace("WIKIPEDIA_SUCHBEGRIFF:", "").strip()
        elif line.startswith("FUN_FACT:"):
            data["fun_fact"] = line.replace("FUN_FACT:", "").strip()
    
    # Mehrzeilige Erklärung sammeln
    if "ERKLAERUNG:" in response:
        erklaerung_start = response.find("ERKLAERUNG:") + len("ERKLAERUNG:")
        erklaerung_ende = response.find("WIKIPEDIA_SUCHBEGRIFF:")
        if erklaerung_ende > erklaerung_start:
            data["erklaerung"] = response[erklaerung_start:erklaerung_ende].strip()
    
    return data

def run_lern_bot():
    print("🎓 Lern-Bot wird gestartet...")
    print(f"📅 {datetime.now().strftime('%A, %d. %B %Y')}")
    print("-" * 60)
    
    config = load_config()
    themen = config.get("themen", ["Physik", "Biologie", "Psychologie"])
    
    # Zufällige Kategorie wählen
    kategorie = random.choice(themen)
    print(f"📚 Kategorie: {kategorie}")
    
    # LLM initialisieren
    llm = LLMClient(config["groq_api_key"])
    
    # Wikipedia + E-Mail initialisieren
    wikipedia = WikipediaAPI("de")
    email = EmailSender(config["email"])
    
    # Lernthema generieren
    print("🧠 Generiere Lernthema...")
    data = generate_lernthema(llm, kategorie)
    
    if not data:
        print("❌ Kein Thema generiert!")
        sys.exit(1)
    
    print(f"   ✅ Thema: {data['thema']}")
    
    # Wikipedia-Artikel holen
    print("📖 Hole Wikipedia-Artikel...")
    wiki_data = wikipedia.get_by_topic(kategorie, data["suchbegriff"])
    
    if wiki_data:
        print(f"   ✅ Wikipedia: {wiki_data['title']}")
    else:
        print("   ⚠️ Kein Wikipedia-Artikel gefunden")
    
    # E-Mail senden
    print("\n📧 Sende E-Mail...")
    success = email.send_lernthema(
        data["thema"],
        kategorie,
        data["erklaerung"],
        wiki_data,
        data["fun_fact"]
    )
    
    if success:
        print("✅ Lernthema erfolgreich gesendet!")
    else:
        print("❌ Fehler beim Senden!")
        # Fallback: Konsole
        print("\n" + "=" * 60)
        print(f"🎓 {kategorie}: {data['thema']}")
        print("=" * 60)
        print(data["erklaerung"])
        print(f"\n💡 Fun Fact: {data['fun_fact']}")

def main():
    if not os.path.exists("config.json"):
        print("❌ config.json nicht gefunden!")
        sys.exit(1)
    
    run_lern_bot()
    
    if "--no-pause" not in sys.argv:
        input("\nDrücke Enter zum Beenden...")

if __name__ == "__main__":
    main()