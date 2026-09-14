 # Folder Organizer CLI

Interaktives Node.js-CLI zum Analysieren und Sortieren von Dateien in kategorisierte Unterordner. Das Tool durchsucht ein Verzeichnis rekursiv und ordnet Dateien anhand ihrer Dateiendung sowie bestimmter Dateinamen ein.

## Voraussetzungen

- Node.js 14 oder neuer

## Installation

```bash
npm install
```

Direkt aus dem Projekt starten:

```bash
npm start
```

Optional kann das CLI global verknüpft werden:

```bash
npm link
folder-organizer
```

## Verwendung

Nach dem Start wartet das Tool auf interaktive Befehle. Jeder Befehl kann mit einem Pfad ergänzt werden. Ohne Pfad wird das aktuelle Verzeichnis verwendet.

| Befehl | Kurzform | Beschreibung |
| --- | --- | --- |
| `preview [pfad]` | `p` | Zeigt die geplante Zuordnung, ohne Dateien zu verschieben |
| `stats [pfad]` | `s` | Zeigt Datei-, Ordner-, Größen- und Kategorie-Statistiken |
| `organize [pfad]` | `o` | Fragt nach Bestätigung und verschiebt die Dateien |
| `path [pfad]` | `cd` | Wechselt das Arbeitsverzeichnis |
| `config` | `c` | Zeigt Kategorien und unterstützte Dateitypen |
| `help` | `h` | Zeigt die Hilfe erneut an |
| `exit` | `q` | Beendet das Programm |

Beispiele:

```text
folder-organizer> preview ./Downloads
folder-organizer> stats ./Documents
folder-organizer> organize C:\Users\Name\Downloads
```

Vor dem Verschieben zeigt das Tool eine Dateivorschau und verlangt eine Bestätigung mit `yes` oder `y`.

## Kategorien

Dateien werden standardmäßig unter anderem diesen Kategorien zugeordnet:

`Images`, `Documents`, `Spreadsheets`, `Presentations`, `Archives`, `Audio`, `Video`, `Code`, `Databases`, `Fonts`, `Config`, `Executables`, `Design`, `Backups`, `Scripts` und `Other`.

Sonderdateien wie `README.md`, `package.json`, `requirements.txt` und `.gitignore` besitzen eine feste Zuordnung. Nicht erkannte Dateien landen in `Other`.

## Verhalten und Sicherheit

- Versteckte Verzeichnisse, `.git`, `node_modules` und `__pycache__` werden übersprungen.
- Bereits vorhandene Kategorieordner werden nicht erneut durchsucht.
- Bei Dateinamenkonflikten wird ein Suffix wie `_1` oder `_2` ergänzt.
- `preview` und `stats` verändern keine Dateien.
- `organize` verschiebt Dateien dauerhaft. Vor der Ausführung sollte ein Backup erstellt oder zuerst `preview` verwendet werden.

## Projektstruktur

```text
bin/index.js       Interaktive CLI und Befehlsverarbeitung
lib/organizer.js   Scan-, Zuordnungs- und Verschiebelogik
```

## Tests

```bash
npm test
```

## Lizenz

MIT
