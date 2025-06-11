from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Database connection settings from environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "todo_db")
DB_USER = os.environ.get("DB_USER", "todo_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "todo_pass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        cur.execute("INSERT INTO todos (title, done) VALUES (%s, %s)", (title, False))
        conn.commit()

    cur.execute("SELECT id, title, done FROM todos ORDER BY id")
    todos = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE todos SET done = NOT done WHERE id = %s", (todo_id,))
    conn.commit()

    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()

    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
