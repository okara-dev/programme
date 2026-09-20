# Motivation Bot

## What It Is

Motivation Bot generates a short, personal morning letter in German with an LLM and sends it by email together with a quote.

## Features

- Personalize the letter with the configured recipient name.
- Include the current weekday, encouragement, and one practical daily tip.
- Fetch and format an additional quote.
- Send HTML and plain-text email content through SMTP.
- Fall back to terminal output if sending fails.
- Use a primary Groq model and an automatic fallback model.

## Usage

Requirements: Python 3.10+, a Groq API key, internet access, and an SMTP account.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

Create a local `config.json` with `groq_api_key`, `name`, and SMTP sender, receiver, password, server, and port. `start_motivation.bat` can be used on Windows after checking its environment. Run from the bot directory.

## Technology

- Python 3.10+
- `groq` for language-model generation
- `requests` and the quote API integration
- SMTP with STARTTLS

## Privacy and Safety

The configured name and prompt are sent to Groq, while the generated letter and quote are sent through the configured SMTP provider. Treat the API key, SMTP password, email addresses, and generated messages as private. Never commit `config.json`; rotate credentials if they have been exposed.

## Distribution

Motivation Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. External service access may be required separately.

## License

No license is currently specified for this project. Obtain permission before redistributing or commercially reusing the source outside the applicable Gumroad terms.

## Status

Version is not declared. Generated motivational content is not medical, psychological, or professional advice.