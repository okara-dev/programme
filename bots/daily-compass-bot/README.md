# Daily Compass Bot

## Zweck

Daily Compass erstellt eine taegliche Nachricht mit Nachrichten, Technik-News, NASA-Inhalten, einem Sprichwort und einem Witz. Die Nachricht wird als HTML- und Plain-Text-E-Mail versendet.

## Inhalte

- RSS-Schlagzeilen aus Tagesschau und Spiegel.
- Top-Stories von Hacker News.
- Beliebte Artikel von Dev.to.
- NASA Astronomy Picture of the Day.
- Ein Zitat aus DummyJSON oder ein lokales Sprichwort als Fallback.
- Ein Witz aus JokeAPI oder ein lokaler deutscher Fallback.
- Automatische Uebersetzung der NASA-Texte, Sprichwoerter und Witze mit DeepL.
- API- und Fallback-Fehler werden abgefangen, damit die Zusammenstellung weiterlaufen kann.

## Installation und Start

Voraussetzungen: Python 3.10+, Internetzugang, ein DeepL-API-Schluessel, ein NASA-API-Schluessel und ein SMTP-Konto.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

`--no-pause` beendet den Prozess ohne abschliessende Eingabeaufforderung und eignet sich fuer geplante Jobs. Unter Windows kann `start_compass.bat` verwendet werden.

## Konfiguration

Lege im Bot-Verzeichnis eine lokale `config.json` mit dieser Struktur an:

```json
{
	"api_keys": {"nasa_api": "..."},
	"deepl_api_key": "...",
	"email": {
		"sender": "...",
		"password": "...",
		"receiver": "...",
		"smtp_server": "smtp.gmail.com",
		"smtp_port": 587
	}
}
```

API-Schluessel, SMTP-Passwoerter und E-Mail-Adressen gehoeren nicht in die Versionsverwaltung. Bei Gmail sollte ein App-Passwort verwendet werden.

## Abhaengigkeiten

- `requests` fuer NASA, Hacker News, Dev.to, Zitate und Witze
- `feedparser` fuer RSS-Feeds
- `deepl` fuer die Uebersetzung
- SMTP mit STARTTLS fuer den Versand

## Lizenz und Status

Eine Lizenz ist derzeit nicht festgelegt. Der Bot ist ein lokales Automatisierungsskript; externe APIs koennen ausfallen oder ihre Antworten aendern.