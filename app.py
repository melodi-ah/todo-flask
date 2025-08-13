from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'todo.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("SELECT id, task, status FROM todo")
        todos = cursor.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO todo (task) VALUES (?)", (task,))
    return redirect(url_for('index'))

@app.route('/done/<int:todo_id>')
def done(todo_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE todo SET status = 'done' WHERE id = ?", (todo_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

