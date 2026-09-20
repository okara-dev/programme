# Sprachlehrer Bot

## What It Is

Sprachlehrer Bot is a daily Spanish vocabulary and grammar assistant for German-speaking learners. It generates 20 new words, adds example sentences, selects a grammar topic, and sends the lesson by email.

## Features

- Configure language and level, currently designed for Spanish and levels such as A1-A2.
- Generate 20 practical vocabulary items with translations and examples.
- Avoid repeating words found in the local vocabulary data.
- Generate a grammar explanation, example, and common learner error.
- Combine generated content with local grammar and vocabulary files.
- Send HTML and plain-text email lessons.
- Fall back to console output when email delivery fails.

## Usage

Requirements: Python 3.10+, a Groq API key, internet access, and an SMTP account.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python main.py --no-pause
```

Keep `config.json`, `grammatik.json`, and `basis_vokabeln.json` in the bot directory. Configure `groq_api_key`, `sprache`, `level`, and SMTP settings. On Windows, `start_lehrer.bat` can be used after checking its environment.

## Technology

- Python 3.10+
- `groq` for language-model generation
- JSON files for local vocabulary and grammar data
- SMTP with STARTTLS

## Privacy and Safety

Learning prompts and configured language settings are sent to Groq. Generated lessons are sent through the configured SMTP provider. Keep API keys, SMTP passwords, recipient addresses, and learner data private. AI-generated translations and grammar explanations should be checked against a trusted source.

## Distribution

Sprachlehrer Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. Groq and email access may require separate accounts.

## License

No license is currently specified for this project. Obtain permission before redistributing or commercially reusing the source outside the applicable Gumroad terms.

## Status

Version is not declared. The current implementation is tailored to Spanish vocabulary and grammar workflows.