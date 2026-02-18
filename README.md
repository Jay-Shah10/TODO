# TODO

A simple to-do list web app built with Flask. Tasks are stored in a local JSON file — no database required.

## Features

- Create, edit, and delete tasks
- Set priority levels (high, medium, low) and optional due dates
- Mark tasks as complete/incomplete
- Filter by status (all, active, completed)
- Sort by creation date, priority, or due date

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app runs at `http://127.0.0.1:5000`.
