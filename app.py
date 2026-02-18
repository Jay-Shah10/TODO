import json
import os
import uuid
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "tasks.json")

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
VALID_PRIORITIES = {"low", "medium", "high"}


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    tasks = load_tasks()
    filter_by = request.args.get("filter", "all")
    sort_by = request.args.get("sort", "created_at")

    if filter_by == "active":
        tasks = [t for t in tasks if not t["completed"]]
    elif filter_by == "completed":
        tasks = [t for t in tasks if t["completed"]]

    if sort_by == "priority":
        tasks.sort(key=lambda t: PRIORITY_ORDER.get(t["priority"], 99))
    elif sort_by == "due_date":
        tasks.sort(key=lambda t: t["due_date"] or "9999-99-99")
    else:
        tasks.sort(key=lambda t: t["created_at"], reverse=True)

    return render_template(
        "index.html", tasks=tasks, filter_by=filter_by, sort_by=sort_by
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template(
                "add.html",
                title=title,
                description=request.form.get("description", ""),
                priority=request.form.get("priority", "medium"),
                due_date=request.form.get("due_date", ""),
            )

        priority = request.form.get("priority", "medium")
        if priority not in VALID_PRIORITIES:
            priority = "medium"

        task = {
            "id": uuid.uuid4().hex[:8],
            "title": title[:120],
            "description": request.form.get("description", "").strip(),
            "priority": priority,
            "due_date": request.form.get("due_date") or None,
            "completed": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)
        flash("Task added.", "success")
        return redirect(url_for("index"))

    return render_template(
        "add.html", title="", description="", priority="medium", due_date=""
    )


@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template(
                "edit.html",
                task={
                    **task,
                    "title": title,
                    "description": request.form.get("description", ""),
                    "priority": request.form.get("priority", task["priority"]),
                    "due_date": request.form.get("due_date", task["due_date"]),
                },
            )

        priority = request.form.get("priority", "medium")
        if priority not in VALID_PRIORITIES:
            priority = "medium"

        task["title"] = title[:120]
        task["description"] = request.form.get("description", "").strip()
        task["priority"] = priority
        task["due_date"] = request.form.get("due_date") or None

        save_tasks(tasks)
        flash("Task updated.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
