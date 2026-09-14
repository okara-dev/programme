 # Folder Structure CLI

Interaktives Node.js-CLI zum Erzeugen von Ordner- und Dateistrukturen aus einer Textdarstellung. Dateien werden mit einfachem Standardinhalt passend zur Dateiendung angelegt.

## Voraussetzungen

- Node.js 14 oder neuer

## Installation

```bash
npm install
```

Das Tool kann direkt aus dem Projekt gestartet werden:

```bash
npm start
```

Optional kann es global verknüpft werden:

```bash
npm link
folder
```

## Verwendung

Nach dem Start wird eine Strukturzeile nach der anderen eingegeben. Eine leere Zeile beendet die Eingabe. Anschließend zeigt das Tool eine Vorschau und fragt nach einer Bestätigung sowie dem Zielpfad.

Beispiel:

```text
my-project/
│
├── src/
│   ├── index.js
│   └── config.json
├── README.md
└── package.json
```

Danach:

```text
✅ Do you want to create this structure? (yes/no): yes
📁 Enter the path where to create the structure: ./output
```

Der Zielpfad ist standardmäßig das aktuelle Verzeichnis. Mit `exit` oder `Ctrl+C` kann die Eingabe beendet werden.

## Unterstützte Standardinhalte

Für einige Dateiendungen wird automatisch ein kurzer Ausgangsinhalt erzeugt, unter anderem für:

- Python, JavaScript und TypeScript
- JSON, YAML und Konfigurationsdateien
- Markdown und Textdateien
- HTML, CSS und Shell-Skripte
- SQL-Dateien

Unbekannte Dateiendungen werden als leere Dateien angelegt. Bereits vorhandene Ordner werden verwendet; vorhandene Dateien werden beim Erzeugen überschrieben.

## Projektstruktur

```text
bin/index.js       Interaktive CLI
lib/generate.js    Parser, Vorschau und Erzeugung
```

## Tests

```bash
npm test
```

## Lizenz

MIT
