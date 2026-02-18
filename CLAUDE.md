# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Activate virtual environment (required before any command)
source venv/bin/activate

# Run the app (dev server with hot-reload on port 5000)
python app.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

Single-file Flask app (`app.py`) serving a dice roller at `http://127.0.0.1:5000`.

- **Routes**: `GET /` renders the page, `POST /roll` returns a JSON result `{"result": N}` where N is 1-6.
- **Templates**: Jinja2 templates in `templates/` extending `base.html`. JavaScript fetch call for rolling without page reload.
- **Styling**: Single `static/style.css`, no CSS framework.
- **Deployment**: Configured for Vercel via `vercel.json` using `@vercel/python` builder.
