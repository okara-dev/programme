"""
Zitate-API – liefert inspirierende Zitate
"""

import requests
import random

class QuoteAPI:
    def __init__(self):
        self.fallback_quotes = [
            ("Das Geheimnis des Erfolgs ist, den Standpunkt des anderen zu verstehen.", "Henry Ford"),
            ("Der einzige Weg, großartige Arbeit zu leisten, ist zu lieben, was du tust.", "Steve Jobs"),
            ("Sei du selbst – alle anderen gibt es schon.", "Oscar Wilde"),
            ("Phantasie ist wichtiger als Wissen.", "Albert Einstein"),
            ("Mut bedeutet nicht, keine Angst zu haben, sondern die Angst zu überwinden.", "Nelson Mandela"),
            ("Das Leben ist zu kurz, um langweilig zu sein.", "Unbekannt"),
            ("Jeder Tag ist eine neue Chance.", "Unbekannt"),
            ("Glaube an dich selbst, auch wenn niemand anders es tut.", "Unbekannt"),
            ("Die einzige Grenze ist die, die du dir selbst setzt.", "Unbekannt"),
            ("In der Mitte der Schwierigkeiten liegen die Möglichkeiten.", "Albert Einstein")
        ]
    
    def get_quote(self):
        """Holt ein zufälliges Zitat"""
        try:
            response = requests.get("https://dummyjson.com/quotes/random", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return {
                    "quote": data.get("quote", "Kein Zitat"),
                    "author": data.get("author", "Unbekannt")
                }
            return self._get_fallback()
        except Exception as e:
            print(f"⚠️ Quote API Fehler: {e} – verwende Fallback")
            return self._get_fallback()
    
    def _get_fallback(self):
        quote, author = random.choice(self.fallback_quotes)
        return {"quote": quote, "author": author}
    
    def format(self, data):
        if not data:
            return "Kein Zitat verfügbar."
        return f"„{data.get('quote', '')}“ — {data.get('author', 'Unbekannt')}"