
# Daily Compass

Der **Daily Compass** erstellt täglich eine kompakte Nachricht mit Nachrichten, einem astronomischen Bild des Tages, einem Fakt, einem Zitat und einem Witz. Die Inhalte werden per E-Mail als HTML- und Textversion verschickt.

## Funktionen

- Top-Nachrichten aus den RSS-Feeds von Tagesschau und Spiegel
- NASA Astronomy Picture of the Day inklusive deutscher Kurzbeschreibung
- Zufälliger Fakt über die Trivia-API mit lokalem Fallback
- Zufälliges Zitat über DummyJSON mit lokalem Fallback
- Sicherer Witz über JokeAPI mit lokalem Fallback
- Versand über einen SMTP-Server, standardmäßig Gmail
- Fortschritts- und Fehlermeldungen im Terminal

Wenn ein externer Dienst nicht erreichbar ist, werden bei Fakt, Zitat und Witz lokale Ersatzinhalte verwendet. Für NASA und RSS wird stattdessen ein Hinweis in der E-Mail angezeigt.

## Voraussetzungen

- Python 3.10 oder neuer
- Internetzugang für die externen APIs und RSS-Feeds
- Ein SMTP-Konto für den E-Mail-Versand

## Installation

Im Verzeichnis dieses Bots:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Falls PowerShell das Aktivieren des virtuellen Environments blockiert, kann der Bot auch direkt mit dem Python-Interpreter aus `.venv` gestartet werden.

## Konfiguration

Lege im Projektverzeichnis eine `config.json` an. Verwende niemals echte Zugangsdaten in einer veröffentlichten README oder in einem Git-Repository.

```json
{
	"api_keys": {
		"trivia_api": "DEIN_TRIVIA_API_KEY",
		"nasa_api": "DEIN_NASA_API_KEY"
	},
	"email": {
		"sender": "absender@example.com",
		"password": "SMTP_PASSWORT_ODER_APP_PASSWORT",
		"receiver": "empfaenger@example.com",
		"smtp_server": "smtp.gmail.com",
		"smtp_port": 587
	},
	"settings": {
		"news_country": "de",
		"news_category": "general",
		"news_max": 5,
		"enable_nasa": true,
		"enable_movie": true,
		"enable_book": true,
		"enable_activity": true,
		"enable_joke": true
	}
}
```

`nasa_api` kann mit einem persönlichen NASA-API-Key oder dem öffentlichen Schlüssel `DEMO_KEY` verwendet werden. Für Gmail wird in der Regel ein App-Passwort benötigt, wenn die Zwei-Faktor-Authentifizierung aktiviert ist.

> Hinweis: Die Einstellungen unter `settings` sind als Konfigurationsschema vorhanden, werden vom aktuellen `main.py` aber noch nicht zur Steuerung der Inhalte ausgewertet. News, NASA, Fakt, Zitat und Witz werden bei jedem Lauf abgerufen.

## Starten

Direkt mit Python:

```powershell
python main.py
```

Der Prozess wartet am Ende auf eine Eingabe. Für automatisierte Aufrufe ohne Pause:

```powershell
python main.py --no-pause
```

Unter Windows kann außerdem `start_compass.bat` verwendet werden. Die Batch-Datei enthält aktuell einen festen lokalen Projektpfad und muss bei einer Installation an einem anderen Ort angepasst werden.

## Automatischer täglicher Versand unter Windows

1. Öffne die **Aufgabenplanung**.
2. Erstelle eine neue Aufgabe mit einem täglichen Trigger.
3. Setze als Programm den Python-Interpreter aus `.venv\Scripts\python.exe`.
4. Setze als Argument `main.py --no-pause`.
5. Setze als Startverzeichnis den Ordner `daily-compass-bot`.

Alternativ kann die Batch-Datei als Aktion verwendet werden. Für einen zuverlässigen Hintergrundlauf sollte sie jedoch ebenfalls auf das gewünschte virtuelle Environment zeigen.

## Projektstruktur

```text
daily-compass-bot/
├── apis/
│   ├── email_sender.py
│   ├── joke_api.py
│   ├── nasa_api.py
│   ├── proverbs_api.py
│   ├── rss_news.py
│   ├── translator.py
│   └── trivia_api.py
├── config.json
├── main.py
├── requirements.txt
└── start_compass.bat
```

## Sicherheit

- Speichere `config.json` nicht in einem öffentlichen Repository.
- Verwende für Gmail ein App-Passwort statt deines normalen Kontopassworts.
- Falls Zugangsdaten bereits geteilt oder committed wurden, widerrufe beziehungsweise rotiere sie sofort.
- Ergänze `config.json` und `.venv/` in `.gitignore`.

Beispiel für `.gitignore`:

```gitignore
config.json
.venv/
__pycache__/
```

## Fehlerbehebung

**`config.json nicht gefunden`**  
Starte den Bot aus seinem Projektverzeichnis und prüfe, ob die Datei dort liegt.

**E-Mail-Versand schlägt fehl**  
Prüfe SMTP-Server, Port, Absender, Empfänger und App-Passwort. Bei Gmail muss SMTP-Zugriff für das verwendete Konto möglich sein.

**Keine externen Inhalte verfügbar**  
Prüfe die Internetverbindung. Für Trivia, Zitate und Witze erscheinen bei API-Fehlern lokale Fallback-Inhalte; NASA und RSS benötigen den jeweiligen Dienst.

## Lizenz

Für dieses Projekt ist derzeit keine Lizenz angegeben.
