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

Single-file Flask app (`app.py`) serving a to-do list at `http://127.0.0.1:5000`.

- **Storage**: JSON file at `data/tasks.json` — read/written via `load_tasks()`/`save_tasks()` helpers in `app.py`. The `data/` directory is auto-created on first write.
- **Routes**: All defined in `app.py` — index (`/`), add, edit, delete, toggle. All mutations use POST; state-changing actions never use GET.
- **Templates**: Jinja2 templates in `templates/` extending `base.html`. No JavaScript — pure HTML forms with POST+redirect.
- **Styling**: Single `static/style.css`, no CSS framework. Priority badges use `.priority-high`/`.priority-medium`/`.priority-low` classes.

## Key Patterns

- Task IDs are 8-char hex strings from `uuid4`. Looked up via linear scan (fine for JSON-scale data).
- Dates stored as ISO strings (`YYYY-MM-DD` for due_date, full ISO for created_at). Null due_date is valid.
- Jinja2 auto-escapes HTML — use real Unicode characters in templates, not HTML entities.
- `filter_by` (all/active/completed) and `sort_by` (created_at/priority/due_date) are query params on the index route.
