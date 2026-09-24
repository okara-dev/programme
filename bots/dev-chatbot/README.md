# Dev-Chat-Bot

## Zweck

Der Dev-Chat-Bot ist ein interaktiver Terminal-Assistent fuer Entwickler. Er durchsucht GitHub und npm, findet freie APIs, erzeugt Charts und fuehrt Websuchen durch.

## Befehle

### GitHub

- `repo facebook/react`: Repository-Informationen wie Sterne, Forks, Issues, Sprache und Lizenz.
- `user torvalds`: Profilinformationen eines GitHub-Benutzers.
- `suche code fastapi`: bis zu fuenf passende Code-Ergebnisse.

### Pakete und APIs

- `npm express`: npm-Paketinformationen und woechentliche Downloads.
- `api weather`: Suche in der Public APIs Directory.

### Charts

QuickChart erzeugt eine URL zu einem Bild. Unterstuetzt werden `bar`, `line` und `pie`:

```text
chart bar Januar,Februar,Maerz 100,200,150
chart line Mo,Di,Mi 5,8,3
chart pie A,B,C 30,50,20
```

Die Anzahl der Labels und Datenwerte muss uebereinstimmen.

### Websuche und Steuerung

- `web python tutorial` oder `such python tutorial`: DuckDuckGo-Websuche.
- `hilfe`: Befehlsuebersicht.
- `exit`, `quit`, `beenden` oder `tschüss`: Bot beenden.

## Installation und Start

Voraussetzungen: Python 3.10+ und Internetzugang.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Unter Windows kann `Dev-Chatbot.bat` verwendet werden. Starte den Bot aus seinem Verzeichnis, damit `config.json` gefunden wird.

## Konfiguration

GitHub funktioniert ohne Token fuer oeffentliche Daten. Ein optionaler Token erhoeht das API-Limit und wird in `config.json` hinterlegt:

```json
{
	"github_token": "..."
}
```

Verwende einen lokalen Token und veroeffentliche die Konfigurationsdatei nicht.

## Abhaengigkeiten und Dienste

- `requests` fuer GitHub, npm und die Public APIs Directory
- `ddgs` fuer die DuckDuckGo-Suche
- GitHub REST API
- npm Registry API
- Public APIs Directory
- QuickChart ohne eigenen API-Schluessel

Suchbegriffe und angeforderte Entwicklungsdaten werden an externe Dienste gesendet. Ergebnisse koennen unvollstaendig oder veraltet sein.

## Lizenz und Status

Eine Lizenz ist derzeit nicht festgelegt. Der Bot gibt Ergebnisse und Chart-URLs im Terminal aus und speichert keine eigenen Verlaufsdaten.
