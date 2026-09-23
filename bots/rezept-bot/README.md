# Snack Bot

## What It Is

Snack Bot is an interactive German-language recipe assistant. It turns ingredients entered in the terminal into a quick mini-snack suggestion and stores optional ratings locally.

## Features

- Generate a snack from user-provided ingredients with an LLM.
- Request a creative name, ingredient list, preparation steps, taste description, and tip.
- Limit the generated recipe to a quick preparation workflow.
- Rate suggestions from 1 to 10 or skip rating.
- Persist snack history in `rating.json`.
- Show total snacks, average score, top-rated snacks, and recent entries.
- Run `stats`, `exit`, or `quit` from the input prompt.

## Usage

Requirements: Python 3.10+ and a Groq API key.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Create a local `config.json` containing `groq_api_key` and an optional display name. Enter ingredients such as `oats, banana, honey, nuts`, enter `stats` for rating history, or enter `exit` to quit.

## Technology

- Python 3.10+
- `groq` for language-model generation
- JSON files for local rating persistence
- No email delivery component

## Privacy and Safety

Ingredient input is sent to Groq to generate the suggestion. Ratings, ingredient input, and generated recipe fields are stored locally in `rating.json`. Do not enter sensitive personal information. AI recipes can be inaccurate or unsuitable for allergies, dietary restrictions, children, or medical conditions; verify ingredients and preparation before eating.

## Distribution

Snack Bot is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms. Groq access may require a separate account.

## License

No license is currently specified for this project. Obtain permission before redistributing or commercially reusing the source outside the applicable Gumroad terms.

## Status

Version is not declared. The tool is a creative suggestion generator, not a nutrition or food-safety authority.