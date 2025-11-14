# NLP Quiz Generator

An AI-powered quiz generator that creates quizzes from text, topics, or uploaded documents. Supports multiple question types (MCQ, True/False, Fill Blank, Math), difficulty levels, semantic validation, and a monitoring dashboard.

## Features

- Generate quizzes from pasted text, predefined topics, or uploaded files
- Question types: `mcq`, `true_false`, `fill_blank`, `math`
- Difficulty classification and weighted scoring
- Validation: normalized matching, WordNet synonyms/lemmas, noun-phrase checks, lightweight cosine similarity, corpus checks
- Math support: symbolic/numeric answer equivalence using `sympy`; LaTeX rendering via MathJax
- Feedback and metrics: flag questions and view validation metrics

## Tech Stack

- Backend: Flask, SQLAlchemy
- NLP: NLTK (tokenization, POS tagging, WordNet)
- Math: SymPy (symbolic/numeric), optional LaTeX parsing
- Frontend: Bootstrap, jQuery, MathJax
- Testing: pytest

## Prerequisites

- Python 3.10+
- Optionally: SQLite (default) or Postgres

## Setup (Windows PowerShell)

```powershell
# 1) Create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install base dependencies
pip install -r requirements.txt

# 3) Install optional/test deps (math & LaTeX parsing, tests)
pip install sympy antlr4-python3-runtime pytest

# 4) (Optional) Pre-download NLTK data
python download_nltk.py

# 5) Configure DB (SQLite default)
$env:DATABASE_URL = "sqlite:///quiz.db"
```

## Run

```powershell
.\.venv\Scripts\python main.py
# App runs on http://localhost:5000/
```

Login is required; create a user via your existing auth flow or seed scripts if available.

## Generate Quizzes

- Home page lets you choose source: Text, Topic, or File Upload
- Select question types; include `Math` to enable math problems with LaTeX text
- Choose difficulty and number of questions

## Testing

```powershell
# Skip full app init during tests to avoid DB wiring
$env:SKIP_APP_INIT = "1"
pytest -q
```

## Configuration

- `DATABASE_URL` (e.g., `sqlite:///quiz.db` or Postgres)
- `.env` supported via `python-dotenv`
- Theme toggle available; metrics page at `/metrics`

## Notes

- If LaTeX parsing is desired for user inputs, ensure `antlr4-python3-runtime==4.11.x` is installed
- NLTK resources are auto-downloaded on demand; use `download_nltk.py` to prefetch
- For Postgres, install `psycopg2-binary` and set `DATABASE_URL` accordingly

## License

This project is provided as-is for educational purposes.