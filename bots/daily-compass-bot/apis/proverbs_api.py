"""
Sprichwörter-API – mit zuverlässiger Quote API
"""

import random
import requests
from .translator import translate_text

class ProverbsAPI:
    def __init__(self):
        self.fallback_proverbs = [
            ("Der beste Zeitpunkt, einen Baum zu pflanzen, war vor 20 Jahren. Der zweitbeste Zeitpunkt ist jetzt.", "Chinesisches Sprichwort"),
            ("Ein langer Weg beginnt mit einem einzigen Schritt.", "Chinesisches Sprichwort"),
            ("Fall sieben Mal, steh acht Mal auf.", "Japanisches Sprichwort"),
            ("Selbst Affen fallen von Bäumen.", "Koreanisches Sprichwort"),
            ("Wenn du eine Frucht isst, denk an den, der den Baum gepflanzt hat.", "Vietnamesisches Sprichwort"),
            ("Lass deinen Schatten nicht über dich wandern.", "Thailändisches Sprichwort"),
            ("Um den Weg vor dir zu kennen, frage die, die zurückkommen.", "Chinesisches Sprichwort"),
            ("Geduld ist die Mutter der Weisheit.", "Chinesisches Sprichwort"),
            ("Wer den Wind sät, wird Sturm ernten.", "Chinesisches Sprichwort"),
            ("Lerne von gestern, lebe für heute, hoffe auf morgen.", "Chinesisches Sprichwort")
        ]
    
    def get_proverb(self):
        """Holt ein zufälliges Zitat (ersetzt Sprichwörter)"""
        try:
            # DummyJSON Quote API – kostenlos, kein Key
            url = "https://dummyjson.com/quotes/random"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                quote = data.get("quote", "Kein Zitat")
                author = data.get("author", "Unbekannt")
                
                return {
                    "proverb": quote,
                    "meaning": f"– {author}",
                    "language": "Weisheit"
                }
            else:
                return self._get_fallback_proverb()
                
        except Exception as e:
            print(f"⚠️ Quote API Fehler: {e} – verwende Fallback")
            return self._get_fallback_proverb()
    
    def _get_fallback_proverb(self):
        proverb, meaning = random.choice(self.fallback_proverbs)
        return {
            "proverb": proverb,
            "meaning": meaning,
            "language": "Sprichwort (lokal)"
        }
    
    def format(self, data):
        if not data:
            return "📜 Kein Sprichwort verfügbar."
        
        proverb = translate_text(data.get("proverb", "Kein Sprichwort"))
        meaning = data.get("meaning", "Keine Bedeutung")
        language = data.get("language", "Unbekannt")
        
        return f"""📜 **SPRICHWORT DES TAGES**

"{proverb}"

📖 Bedeutung: {meaning}

🌏 Sprache: {language}"""