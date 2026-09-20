# Daily Compass Bot

## What It Is

Daily Compass is a Python newsletter bot that builds a compact daily briefing and sends it by email in both HTML and plain-text formats.

## Features

- Collect headlines from configured RSS feeds.
- Fetch NASA's Astronomy Picture of the Day.
- Add a proverb or fact and a joke, with local fallback content where supported.
- Send one formatted message through an SMTP server.
- Continue with fallback content when selected external services are unavailable.
- Run interactively or without the final pause for scheduled jobs.

## Usage

Requirements: Python 3.10+, internet access, and an SMTP account.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

Create a local `config.json` with API keys, SMTP sender/receiver settings, and server details. Never publish that file. On Windows, `start_compass.bat` can be used after checking its working-directory and interpreter settings. For daily delivery, schedule `main.py --no-pause` with Windows Task Scheduler.

## Technology

- Python 3.10+
- `requests`, `feedparser`, and `deep-translator`
- NASA and RSS integrations
- SMTP with STARTTLS for email delivery

## Privacy and Safety

The bot sends collected content and generated email data through the configured external services and SMTP provider. The configured recipient receives the briefing. API keys, SMTP passwords, email addresses, and generated content must be treated as private. Use an app password where supported, keep `config.json` out of version control, and rotate credentials if exposed.

## Distribution

Daily Compass Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. External API accounts and email service access may be required separately.

## License

No license is currently specified for this project. Do not redistribute or modify it commercially without obtaining permission or adding clear licensing terms.

## Status

Current version is an automation script. Settings such as content toggles are present in the configuration schema but are not all enforced by the current `main.py` implementation.