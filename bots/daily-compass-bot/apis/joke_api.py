import requests
import random

class JokeAPI:
    def __init__(self):
        self.base_url = "https://v2.jokeapi.dev/joke"
        
        # Deutsche Witze (Fallback)
        self.german_jokes = [
            "Warum hat der Programmierer keinen Hund? Weil er schon genug Fehler im Code hat! 😄",
            "Warum können Geister so gut programmieren? Weil sie viel 'Pointer'-Erfahrung haben! 👻"
        ]
    
    def get_joke(self, category="Any"):
        params = {
            "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit",
            "safe-mode": "true",
            "type": "single"
        }
        
        try:
            response = requests.get(f"{self.base_url}/{category}", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("error"):
                return self._get_fallback_joke()
            
            # KEINE Übersetzung – Witz bleibt auf Englisch
            return data
            
        except Exception as e:
            print(f"❌ JokeAPI Fehler: {e}")
            return self._get_fallback_joke()
    
    def _get_fallback_joke(self):
        return {
            "joke": random.choice(self.german_jokes),
            "category": "Deutsch"
        }
    
    def format(self, data):
        if not data:
            return "😂 Kein Witz verfügbar."
        
        joke = data.get("joke", "Kein Witz")
        category = data.get("category", "Unbekannt")
        
        category_map = {
            "Programming": "Programmierung",
            "Pun": "Wortspiel",
            "Misc": "Verschiedenes",
            "Deutsch": "🇩🇪 Deutsch"
        }
        category_de = category_map.get(category, category)
        
        return f"""😂 **WITZ DES TAGES**

{joke}

📂 Kategorie: {category_de}"""