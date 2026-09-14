# Vulnerability Scanner CLI

Sicherheits-Scanner für Projekt-Schwachstellen. Prüft auf bekannte Sicherheitslücken in Dependencies, Code-Probleme, exponierte Umgebungsdateien und Secrets.

## Installation

```bash
npm install
```

## Nutzung

### Basis-Scan
```bash
npm start
# oder
npm start -- --path ./
```

### Interaktiver Modus
```bash
npm start -- --interactive
```

### Mit spezifischen Checks
```bash
npm start -- --npm --code --env --secrets
# oder Kurzform
npm start -- --all
```

## Optionen

| Option | Kurz | Standard | Beschreibung |
|--------|------|----------|-------------|
| `--path` | `-p` | `./` | Pfad zum Projekt |
| `--format` | `-f` | `table` | Ausgabeformat: `json`, `table`, `html` |
| `--output` | `-o` | - | Ausgabedatei für Report |
| `--interactive` | `-i` | - | Interaktiver Modus |
| `--npm` | - | - | Nur NPM Dependencies prüfen |
| `--code` | - | - | Nur Code-Analyse |
| `--env` | - | - | Nur Environment-Dateien |
| `--secrets` | - | - | Nur Secrets detektieren |
| `--all` | - | - | Alle Checks ausführen |

## Beispiele

```bash
# Vollständiger Scan des aktuellen Projekts
npm start

# Scan eines anderen Projekts
npm start -- --path /path/to/project

# Nur NPM-Vulnerabilities
npm start -- --npm

# JSON-Report speichern
npm start -- --format json --output ./security-report.json

# Interaktive Auswahl der Checks
npm start -- --interactive
```

## Sicherheits-Checks

### 1. NPM Audit 🔒
- Überprüft bekannte Schwachstellen in Dependencies
- Nutzt `npm audit`
- Bewertet Severity: critical, high, medium, low

### 2. Code Analysis 🔍
- Sucht nach unsicheren Coding-Patterns
- Erkennt: eval(), dynamic requires, innerHTML, SQL-Injection-Muster
- Hardcoded Secrets erkennen

### 3. Environment Check 🔑
- Prüft auf nicht-ignorierte .env Dateien
- Warnt vor sensiblen Dateien (AWS, SSH, Docker-Configs)
- Empfiehlt .gitignore-Einträge

### 4. Secrets Detection 🕵️
- Scannt Code nach exponierten Secrets
- Erkennt: API Keys, Tokens, Private Keys, OAuth-Tokens
- Warnt vor Hardcoded-Credentials

## Ausgabeformate

### Table (Standard)
```
🔒 Security Vulnerability Scanner

📊 Scan Results:

Total Issues: 5
  🔴 Critical: 2
  🟠 High: 1
  🟡 Medium: 2

🔍 Issues Found:

🔴 [CRITICAL] NPM Dependency Vulnerability: express
   Type: npm-vulnerability
   ...
```

### JSON
```json
{
  "projectPath": "/path/to/project",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "issues": [...],
  "summary": {...}
}
```

## Severity-Levels

- 🔴 **CRITICAL** - Sofort beheben erforderlich
- 🟠 **HIGH** - Schnell beheben empfohlen
- 🟡 **MEDIUM** - Zeitnah beheben
- 🔵 **LOW** - Bei Gelegenheit überprüfen

## Exit Codes

- `0` - Erfolgreich, keine kritischen Probleme
- `1` - Fehler während Scan
- `2` - Kritische Vulnerabilities gefunden

## Features

- 🚀 Schnelle Sicherheitsprüfung
- 🔍 Mehrere Scan-Typen (NPM, Code, Env, Secrets)
- 📊 Detaillierte Reports
- 💾 Export zu JSON/HTML
- 🎨 Farbige Terminal-Ausgabe
- 🤖 Automatisierbar für CI/CD

## Use Cases

### Vor Production-Deployment
```bash
npm start -- --path ./ --format json --output ./deploy-scan.json
```

### CI/CD Integration
```bash
npm start -- --all --format json > ./security-report.json
if grep -q "critical" security-report.json; then exit 1; fi
```

### Regelmäßige Audits
```bash
npm start -- --npm  # Nur Dependencies
```

## Best Practices

1. **Regelmäßig scannen** - Mindestens wöchentlich
2. **.gitignore überprüfen** - Stellt sicher, dass Secrets nicht committed werden
3. **Secrets Management** - Nutze Environment-Variablen für Credentials
4. **Dependencies aktuell halten** - Regelmäßige Updates
5. **Code Reviews** - Checke Scanner-Warnungen

## Limitations

- Code-Analyse ist Pattern-basiert (keine AST-Analyse)
- NPM Audit ist abhängig von npm-Registry
- Secrets-Detection basiert auf Regex-Patterns

## Dependencies

- `commander` - CLI-Argument-Parser
- `inquirer` - Interaktive CLI-Prompts
- `chalk` - Farbige Terminal-Ausgabe
- `axios` - HTTP-Client für API-Checks
- `table` - Tabellen-Formatierung

## Lizenz

MIT

---

**Hinweis:** Dieses Tool sollte als Teil eines umfassenden Sicherheitsprozesses verwendet werden, nicht als einziges Sicherheits-Tool.
