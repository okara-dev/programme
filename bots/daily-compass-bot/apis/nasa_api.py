import requests
from .translator import translate_text

class NASAAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov"
    
    def get_apod(self):
        url = f"{self.base_url}/planetary/apod"
        params = {"api_key": self.api_key}
        
        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ NASA API Fehler: {e}")
            return None
    
    def format(self, data):
        if not data:
            return "🚀 Keine NASA-Daten verfügbar."
        
        title = data.get("title", "Unbekannt")
        date = data.get("date", "Unbekannt")
        explanation = data.get("explanation", "Keine Beschreibung")
        url = data.get("url", "#")
        hd_url = data.get("hdurl", url)
        
        # Übersetzen
        title_de = translate_text(title)
        explanation_de = translate_text(explanation)
        explanation_short = explanation_de[:400] + "..." if len(explanation_de) > 400 else explanation_de
        
        return f"""🚀 **NASA: Astronomisches Bild des Tages**
📅 {date}
📷 **{title_de}**

{explanation_short}

🔗 [Bild ansehen]({url})
🖼️ [HD Bild]({hd_url})"""