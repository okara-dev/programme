"""
Übersetzung mit DeepL API
Free-Tier: 500.000 Zeichen/Monat kostenlos 
"""

import deepl

class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = deepl.DeepLClient(api_key)
        print("✅ DeepL Translator initialisiert")
    
    def translate(self, text, target_lang="DE"):
        if not text:
            return text
        try:
            result = self.client.translate_text(text, target_lang=target_lang)
            return result.text
        except Exception as e:
            print(f"⚠️ DeepL Fehler: {e}")
            return text
    
    def translate_batch(self, texts, target_lang="DE"):
        if not texts:
            return texts
        try:
            results = self.client.translate_text(texts, target_lang=target_lang)
            return [r.text for r in results]
        except Exception as e:
            print(f"⚠️ DeepL Batch Fehler: {e}")
            return texts
    
    def get_usage(self):
        try:
            usage = self.client.get_usage()
            if usage.character.valid:
                print(f"📊 DeepL: {usage.character.count}/{usage.character.limit} Zeichen verbraucht")
                return usage
        except Exception as e:
            print(f"⚠️ DeepL Usage Fehler: {e}")
        return None


# === GLOBALE INSTANZ (für andere Module) ===
_translator = None

def init_translator(api_key):
    """Initialisiert den globalen Translator (einmal in main.py aufrufen)"""
    global _translator
    _translator = Translator(api_key)
    return _translator

def translate_text(text, target_lang="DE"):
    """Globale Übersetzungsfunktion (von rss_news, nasa_api etc. genutzt)"""
    if _translator is None:
        return text
    return _translator.translate(text, target_lang)