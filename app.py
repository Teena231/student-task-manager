from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            category TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY completed, due_date"
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending = total - completed

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]
    assigned_to = request.form["assigned_to"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]
    category = request.form["category"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO tasks
        (title, assigned_to, priority, due_date, category)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        assigned_to,
        priority,
        due_date,
        category
    ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    conn = get_db_connection()

    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

init_db()

if __name__ == "__main__":
    app.run(debug=True)