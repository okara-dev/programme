"""
Open Food Facts API – Lebensmittelprodukte & Nährwerte
Kostenlos, kein Key nötig
"""

import requests
import time

class OpenFoodFactsAPI:
    def __init__(self):
        self.base_url = "https://world.openfoodfacts.org"
        self.headers = {
            "User-Agent": "SnackBot/1.0 (https://github.com/okara-dev)"
        }
    
    def search_product(self, name, retries=3):
        """Sucht ein Produkt nach Namen (mit Retry)"""
        # Bereinige den Suchbegriff (entferne Sonderzeichen)
        name = name.strip().rstrip("#").strip()
        
        for attempt in range(retries):
            try:
                response = requests.get(
                    f"{self.base_url}/cgi/search.pl",
                    params={
                        "search_terms": name,
                        "search_simple": 1,
                        "action": "process",
                        "json": 1,
                        "page_size": 1
                    },
                    headers=self.headers,
                    timeout=15
                )
                
                # Bei 503: warten und erneut versuchen
                if response.status_code == 503:
                    if attempt < retries - 1:
                        wait_time = (attempt + 1) * 2
                        print(f"   ⏳ Server überlastet, warte {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return None
                
                response.raise_for_status()
                data = response.json()
                products = data.get("products", [])
                return products[0] if products else None
                
            except requests.exceptions.Timeout:
                if attempt < retries - 1:
                    print(f"   ⏳ Timeout, versuche erneut...")
                    time.sleep(2)
                    continue
                return None
            except Exception as e:
                print(f"⚠️ Open Food Facts Fehler: {e}")
                return None
        
        return None
    
    def format(self, product):
        if not product:
            return "🥗 Kein Produkt gefunden (API evtl. überlastet – später erneut versuchen)."
        
        name = product.get("product_name", "Unbekannt")
        brand = product.get("brands", "?")
        quantity = product.get("quantity", "?")
        
        nutriments = product.get("nutriments", {})
        energy = nutriments.get("energy-kcal_100g", "?")
        fat = nutriments.get("fat_100g", "?")
        carbs = nutriments.get("carbohydrates_100g", "?")
        proteins = nutriments.get("proteins_100g", "?")
        salt = nutriments.get("salt_100g", "?")
        sugar = nutriments.get("sugars_100g", "?")
        
        nutriscore = product.get("nutriscore_grade", "?").upper()
        allergens = product.get("allergens", "")
        
        return f"""
🥗 **{name}**

🏢 Marke: {brand}
⚖️ Menge: {quantity}

📊 **Nährwerte pro 100g:**
   🔥 Kalorien: {energy} kcal
   🧈 Fett: {fat} g
   🍞 Kohlenhydrate: {carbs} g
   🍬 Zucker: {sugar} g
   🥩 Proteine: {proteins} g
   🧂 Salz: {salt} g

🏆 Nutri-Score: {nutriscore}
⚠️ Allergene: {allergens if allergens else "Keine"}
"""