"""
Zentrale Übersetzungs-Funktion für alle APIs
Mit Cache, Limit & intelligenter Übersetzung
"""

import time

class Translator:
    def __init__(self):
        self.translator = None
        self.available = False
        self.cache = {}  # Übersetzungs-Cache
        self.translation_count = 0
        self.max_translations_per_run = 5  # Max. 5 Übersetzungen pro Bot-Durchlauf
        
        # Versuche deep-translator zu laden
        try:
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator(source='en', target='de')
            self.available = True
            print("✅ Übersetzer initialisiert (deep-translator)")
        except Exception as e:
            print(f"⚠️ Übersetzer nicht verfügbar: {e}")
            print("   Verwende Fallback-Übersetzungen")
            self.available = False
    
    def translate(self, text):
        """
        Übersetzt einen Text von Englisch nach Deutsch
        Mit Cache und Limit
        """
        if not text:
            return text
        
        # Übersetzer nicht verfügbar → Fallback
        if not self.available:
            return self._simple_fallback(text)
        
        # Cache prüfen
        if text in self.cache:
            return self.cache[text]
        
        # Limit prüfen
        if self.translation_count >= self.max_translations_per_run:
            return self._simple_fallback(text)
        
        # NUR kurze Texte übersetzen (< 300 Zeichen)
        if len(text) > 300:
            return self._simple_fallback(text)
        
        try:
            # Übersetzen
            translated = self.translator.translate(text)
            
            # Prüfen ob Übersetzung sinnvoll ist
            if translated and len(translated) > 3 and translated != text:
                self.cache[text] = translated
                self.translation_count += 1
                return translated
            else:
                return self._simple_fallback(text)
                
        except Exception as e:
            print(f"⚠️ Übersetzungsfehler: {e}")
            return self._simple_fallback(text)
    
    def _simple_fallback(self, text):
        """Einfache Fallback-Übersetzung für häufige englische Begriffe"""
        replacements = {
            "Title": "Titel",
            "Year": "Jahr",
            "Genre": "Genre",
            "Director": "Regisseur",
            "Actors": "Schauspieler",
            "Plot": "Handlung",
            "Rating": "Bewertung",
            "Author": "Autor",
            "Published": "Veröffentlicht",
            "Pages": "Seiten",
            "Publisher": "Verlag",
            "Country": "Land",
            "Category": "Kategorie",
            "Participants": "Teilnehmer",
            "Price": "Preis",
            "Accessibility": "Zugänglichkeit",
            "Activity": "Aktivität",
            "Type": "Typ",
            "Source": "Quelle",
            "Language": "Sprache",
            "Description": "Beschreibung",
            "Date": "Datum",
            "Time": "Uhrzeit",
            "Link": "Link",
            "Image": "Bild",
            "Video": "Video",
            "Music": "Musik",
            "Book": "Buch",
            "Movie": "Film",
            "News": "Nachrichten",
            "NASA": "NASA",
            "Joke": "Witz",
            "Compass": "Kompass",
            "Daily": "Täglich",
            "Briefing": "Briefing",
            "Update": "Update",
            "Available": "Verfügbar",
            "Unknown": "Unbekannt",
            "None": "Keine",
            "Not found": "Nicht gefunden",
            "Error": "Fehler",
            "Success": "Erfolg",
            "Warning": "Warnung",
            "Info": "Information",
            "Please": "Bitte",
            "Thank you": "Danke",
            "Hello": "Hallo",
            "Goodbye": "Auf Wiedersehen",
            "Welcome": "Willkommen",
            "Moon": "Mond",
            "Star": "Stern",
            "Planet": "Planet",
            "Galaxy": "Galaxie",
            "Space": "Weltraum",
            "Astronomy": "Astronomie",
            "Solar System": "Sonnensystem",
            "Earth": "Erde",
            "Mars": "Mars",
            "Jupiter": "Jupiter",
            "Saturn": "Saturn",
            "Uranus": "Uranus",
            "Neptune": "Neptun",
            "Pluto": "Pluto"
        }
        
        for eng, deu in replacements.items():
            text = text.replace(eng, deu)
        
        return text
    
    def reset_count(self):
        """Setzt den Übersetzungszähler zurück (für neuen Bot-Durchlauf)"""
        self.translation_count = 0

# Globale Instanz
translator = Translator()

def translate_text(text):
    """Globale Übersetzungsfunktion"""
    return translator.translate(text)

def reset_translator():
    """Setzt den Übersetzungszähler zurück"""
    translator.reset_count()