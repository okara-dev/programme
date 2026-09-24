# Snack-Bot

## Zweck

Snack-Bot ist ein interaktiver deutschsprachiger Lebensmittel- und Rezeptassistent. Er kann KI-Snacks aus Zutaten erzeugen, Rezepte und Cocktails suchen und Produktnaehrwerte anzeigen.

## Befehle

- `snack haferflocken, banane, honig`: KI erzeugt einen schnellen Mini-Snack mit Zutaten, Zubereitung, Geschmack und Tipp.
- `rezept pizza` oder `zufall rezept`: Rezept aus TheMealDB.
- `cocktail mojito` oder `zufall cocktail`: Cocktail aus TheCocktailDB.
- `produkt nutella`: Produkt- und Naehrwertsuche ueber Open Food Facts.
- `stats`: gespeicherte Snack-Bewertungen anzeigen.
- `hilfe`: Befehlsuebersicht.
- `exit`, `quit` oder `beenden`: Bot beenden.

Nach jedem generierten KI-Snack kann eine Bewertung von 1 bis 10 gespeichert oder mit `s` uebersprungen werden.

## Installation und Start

Voraussetzungen: Python 3.10+, Internetzugang und ein Groq-API-Schluessel.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Unter Windows kann `snackBot.bat` verwendet werden. Lege eine lokale `config.json` mit `groq_api_key` an:

```json
{
	"groq_api_key": "..."
}
```

## Lokale Daten und Dienste

- `rating.json` speichert Snack-Eingaben, generierte Daten und Bewertungen.
- `groq` generiert KI-Snacks mit einem automatischen Modell-Fallback.
- TheMealDB liefert Rezepte.
- TheCocktailDB liefert Cocktails.
- Open Food Facts liefert Produkt- und Naehrwertdaten.

Zutaten und Suchbegriffe werden an externe Dienste gesendet. `rating.json` kann persoenliche Eingaben enthalten und sollte nicht veroeffentlicht werden. KI-Vorschlaege, Allergene und Naehrwerte vor der Verwendung pruefen.

## Lizenz und Status

Eine Lizenz ist derzeit nicht festgelegt. Der Bot ist ein kreativer Assistent und keine medizinische oder lebensmittelrechtliche Beratung.