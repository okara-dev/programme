# Lern-Bot

## What It Is

Lern-Bot is a German-language daily learning assistant. It uses Groq-hosted language models to choose and explain a topic from physics, biology, or psychology, enriches it with Wikipedia information, and sends the lesson by email.

## Features

- Choose a learning category from the configured topic list.
- Generate an accessible explanation and a surprising fact with an LLM.
- Query German Wikipedia for a related article and optional thumbnail.
- Create HTML and plain-text email versions.
- Fall back to console output when email delivery fails.
- Use a primary Groq model with an automatic fallback model.

## Usage

Requirements: Python 3.10+, a Groq API key, internet access, and an SMTP account.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

Create a local `config.json` with `groq_api_key`, learning topics, learner name, and SMTP settings. `start_lernbot.bat` can be used on Windows after checking its environment. Run from the bot directory so `config.json` is found.

## Technology

- Python 3.10+
- `groq` for LLM generation
- `requests` and the Wikipedia API integration
- SMTP with STARTTLS

## Privacy and Safety

Prompts and configuration data are sent to Groq when generating a lesson. The generated lesson and Wikipedia data are sent through the configured SMTP provider. Do not include confidential personal data in prompts. Keep API keys, SMTP passwords, and recipient addresses out of source control and rotate exposed credentials.

## Distribution

Lern-Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. Groq, Wikipedia, and email access may require separate accounts or service availability.

## License

No license is currently specified for this project. Obtain permission before redistributing it or using it commercially outside the applicable Gumroad terms.

## Status

Version is not declared. AI explanations and external reference content should be checked before being used as authoritative educational material.