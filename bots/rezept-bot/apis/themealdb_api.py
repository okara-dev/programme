"""
TheMealDB API – Rezepte mit Bildern & Zutaten
Kostenlos, kein Key nötig
"""

import requests

class TheMealDBAPI:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def search_recipe(self, name):
        """Sucht Rezept nach Namen"""
        try:
            response = requests.get(
                f"{self.base_url}/search.php",
                params={"s": name},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            meals = data.get("meals", [])
            return meals[0] if meals else None
        except Exception as e:
            print(f"⚠️ TheMealDB Fehler: {e}")
            return None
    
    def get_random_recipe(self):
        """Holt ein zufälliges Rezept"""
        try:
            response = requests.get(
                f"{self.base_url}/random.php",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            meals = data.get("meals", [])
            return meals[0] if meals else None
        except Exception as e:
            print(f"⚠️ TheMealDB Fehler: {e}")
            return None
    
    def format(self, meal):
        if not meal:
            return "🍔 Kein Rezept gefunden."
        
        name = meal.get("strMeal", "Unbekannt")
        category = meal.get("strCategory", "?")
        area = meal.get("strArea", "?")
        instructions = meal.get("strInstructions", "Keine Anleitung")
        image = meal.get("strMealThumb", "")
        youtube = meal.get("strYoutube", "")
        
        # Zutaten sammeln
        ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}", "")
            measure = meal.get(f"strMeasure{i}", "")
            if ing and ing.strip():
                ingredients.append(f"{measure.strip()} {ing.strip()}".strip())
        
        ing_str = "\n   • " + "\n   • ".join(ingredients) if ingredients else "Keine Zutaten"
        
        # Anleitung kürzen
        if len(instructions) > 1000:
            instructions = instructions[:1000] + "..."
        
        result = f"""
🍔 **{name}**

📂 Kategorie: {category}
🌍 Herkunft: {area}

🖼️ Bild: {image}

📋 **Zutaten:**
   • {ing_str}

👨‍🍳 **Zubereitung:**
{instructions}
"""
        if youtube:
            result += f"\n🎥 Video: {youtube}"
        
        return result