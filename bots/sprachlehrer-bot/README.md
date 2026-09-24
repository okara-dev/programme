# Sprachlehrer-Bot

## Zweck

Der Sprachlehrer-Bot erstellt eine taegliche Spanisch-Lektion fuer deutschsprachige Lernende. Er generiert neue Vokabeln und ein Grammatikthema, mischt lokale Lerninhalte dazu und versendet die Lektion per E-Mail.

## Funktionen

- Generiert 20 neue Vokabeln mit spanischem Wort, deutscher Uebersetzung und Beispielsatz.
- Beruecksichtigt bekannte Vokabeln aus `basis_vokabeln.json`, damit sie nicht erneut vorgeschlagen werden.
- Generiert ein Grammatikthema mit Erklaerung, Beispiel und typischem Fehler.
- Fuegt das KI-Thema und bis zu zwei lokale Grammatikthemen zusammen.
- Versendet HTML- und Plain-Text-Versionen.
- Gibt die Vokabeln in der Konsole aus, wenn der E-Mail-Versand fehlschlaegt.

## Installation und Start

Voraussetzungen: Python 3.10+, Internetzugang, ein Groq-API-Schluessel und ein SMTP-Konto.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

`--no-pause` ueberspringt die abschliessende Eingabeaufforderung. Unter Windows kann `start_lehrer.bat` verwendet werden.

## Dateien und Konfiguration

`config.json`, `grammatik.json` und `basis_vokabeln.json` muessen im Bot-Verzeichnis liegen. Die Konfiguration benoetigt mindestens:

```json
{
	"groq_api_key": "...",
	"sprache": "Spanisch",
	"level": "A1-A2",
	"email": {
		"sender": "...",
		"password": "...",
		"receiver": "...",
		"smtp_server": "smtp.gmail.com",
		"smtp_port": 587
	}
}
```

Die lokalen JSON-Dateien liefern Grammatik und Basisvokabeln. API-Schluessel, SMTP-Passwoerter, E-Mail-Adressen und Lerndaten muessen privat bleiben.

## Abhaengigkeiten und Status

- `groq` mit einem automatischen Modell-Fallback
- SMTP mit STARTTLS
- Lokale JSON-Dateien fuer Lerninhalte

Die aktuellen Daten sind auf Spanisch mit dem Niveau `A1-A2` ausgerichtet. KI-Uebersetzungen und Grammatikangaben sollten geprueft werden.

Eine Lizenz ist derzeit nicht festgelegt.