# Story Bot

## What It Is

Story Bot generates a new short German story each day with a randomly selected theme and genre, then sends the title, story, and moral by email.

## Features

- Choose from a pool of story themes and genres.
- Generate approximately 400-500 words of atmospheric fiction.
- Request a title, narrative, turning point, and closing moral.
- Send HTML and plain-text email content through SMTP.
- Fall back to terminal output when email delivery fails.
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

Create a local `config.json` with `groq_api_key`, recipient name, story settings, and SMTP sender, receiver, password, server, and port. `start_story.bat` can be used on Windows after checking its environment. Run from the bot directory.

## Technology

- Python 3.10+
- `groq` for language-model generation
- JSON configuration
- SMTP with STARTTLS

## Privacy and Safety

The configured name and story prompt are sent to Groq. Generated stories are sent through the configured SMTP provider. Keep credentials and recipient addresses private. Generated content may be inaccurate, unsuitable for some audiences, or similar to common genre patterns; review it before publication.

## Distribution

Story Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. Groq and email access may require separate accounts.

## License

No license is currently specified for this project. Obtain permission before redistributing or commercially reusing the source outside the applicable Gumroad terms.

## Status

Version is not declared. The configured story settings are available in `config.json`; the current implementation selects its own random theme and genre for each run.