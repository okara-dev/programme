# Programme und Automatisierung

In diesem Ordner entwickle ich lokale Programme, Kommandozeilenwerkzeuge, Bots und Spiele. Der Schwerpunkt liegt auf praktischen Helfern für den Entwicklungsalltag, Automatisierung und eigenen Experimenten.


## Struktur

### `bots/`
Automatisierte Programme, die regelmäßig Informationen abrufen, verarbeiten oder als Bericht ausgeben.

### `cli/`
Kommandozeilenprogramme für wiederkehrende Aufgaben beim Entwickeln und Verwalten von Dateien oder Projekten.

### `games/`
Eigene Fun Spiele und interaktive Experimente.


### `shell-befehle/`

Gesammelte und selbst entwickelte Shell-Hilfen für Windows PowerShell und wiederkehrende Aufgaben. Der zentrale Einstieg ist `shell_toolbox.ps1`.


## Typischer Technologie-Stack

- Python für Bots 
- Node.js und JavaScript für CLI-Werkzeuge
- PowerShell für Windows-Automatisierung
- Spieleentwicklung mit 2D- und 3D-Technologien je nach Projekt

## Arbeiten mit einem Programm

Jedes Projekt ist möglichst eigenständig. Deshalb zuerst die README und danach die Projektdateien wie `package.json`, `requirements.txt` oder `config.json` prüfen.

Für Node.js-Projekte:

```bash
npm install
npm start
```

Für Python-Projekte:

```bash
pip install -r requirements.txt
python main.py
```

Einige Programme benötigen zusätzliche lokale Werkzeuge oder API-Schlüssel. Diese werden nicht fest in den Quellcode geschrieben, sondern über Konfigurationsdateien oder Umgebungsvariablen bereitgestellt.
