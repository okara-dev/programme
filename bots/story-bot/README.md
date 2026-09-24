# Story-Bot

## Zweck

Der Story-Bot erstellt bei jedem Lauf eine neue deutschsprachige Kurzgeschichte und versendet sie per E-Mail. Thema und Genre werden aus lokalen Listen zufaellig ausgewaehlt.

## Funktionen

- Zufaellige Auswahl aus zwolf Themen und sechs Genres.
- Generiert eine Geschichte mit etwa 400 bis 500 Woertern.
- Erwartet Titel, Geschichte und Moral in einem festen Antwortformat.
- Versendet HTML- und Plain-Text-Versionen ueber SMTP.
- Gibt die Geschichte in der Konsole aus, wenn der E-Mail-Versand fehlschlaegt.
- Verwendet ein primaeres Groq-Modell und ein automatisches Fallback-Modell.

## Installation und Start

Voraussetzungen: Python 3.10+, Internetzugang, ein Groq-API-Schluessel und ein SMTP-Konto.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

`--no-pause` ueberspringt die abschliessende Eingabeaufforderung. Unter Windows kann `start_story.bat` verwendet werden. Starte den Bot aus seinem Verzeichnis, damit `config.json` gefunden wird.

## Konfiguration

Die lokale `config.json` benoetigt `groq_api_key` und einen `email`-Block:

```json
{
	"groq_api_key": "...",
	"email": {
		"sender": "...",
		"password": "...",
		"receiver": "...",
		"smtp_server": "smtp.gmail.com",
		"smtp_port": 587
	}
}
```

`story_settings` kann in der Datei stehen, wird vom aktuellen `main.py` jedoch nicht zur Auswahl von Thema, Genre oder Laenge verwendet. Diese Werte werden derzeit aus den lokalen Listen und dem Prompt bestimmt.

## Datenschutz und Status

Der Story-Prompt wird an Groq gesendet, die fertige Geschichte an den konfigurierten SMTP-Dienst. API-Schluessel, SMTP-Passwoerter und Empfaengeradressen muessen privat bleiben. KI-generierte Inhalte vor der Weitergabe pruefen.

Abhaengigkeit: `groq>=0.11.0`. Eine Lizenz ist derzeit nicht festgelegt.