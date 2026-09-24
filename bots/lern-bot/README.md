# Lern-Bot

## Zweck

Lern-Bot ist ein interaktiver deutschsprachiger Recherche-Chat fuer kurze Lernfragen. Antworten kommen aus Wikipedia, Open Library oder einer DuckDuckGo-Websuche und werden direkt im Terminal angezeigt.

## Befehle

- `wiki Einstein`, `info Japan` oder `ueber Python`: Wikipedia-Zusammenfassung.
- `thema physik`, `zufall biologie` oder `random informatik`: zufaelliges Thema aus Wikipedia.
- `buch psychologie` oder `buch informatik`: passende Buecher aus Open Library.
- `such python tutorial` oder `google flask`: Websuche ueber DuckDuckGo.
- `hilfe`: Befehlsuebersicht.
- `exit`, `quit`, `tschüss` oder `ciao`: Bot beenden.

Ein einzelnes unbekanntes Wort wird als Wikipedia-Suche behandelt.

## Installation und Start

Voraussetzungen: Python 3.10+ und Internetzugang. Ein LLM- oder SMTP-Konto ist nicht erforderlich.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Unter Windows kann `lernbot.bat` verwendet werden. Starte den Bot aus seinem Verzeichnis, damit `config.json` gefunden wird.

## Konfiguration

Die lokale `config.json` kann optional `sprache` enthalten. Standard ist `de`:

```json
{
	"sprache": "de"
}
```

## Abhaengigkeiten und Datenschutz

- `requests` fuer Wikipedia und Open Library
- `duckduckgo-search` fuer die Websuche

Suchbegriffe werden an die jeweils verwendeten externen Dienste gesendet. Gib keine vertraulichen Informationen ein. Ergebnisse externer Wissensquellen koennen unvollstaendig oder veraltet sein.

## Lizenz und Status

Eine Lizenz ist derzeit nicht festgelegt. Der Bot arbeitet interaktiv im Terminal und versendet keine E-Mails.