#!/usr/bin/env python3
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash

app = Flask(__name__, static_folder='static')
app.config['DATABASE'] = 'tasks.db'
app.config['SECRET_KEY'] = 'dev'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())
    # Ensure changes are committed
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

@app.before_request
def ensure_db():
    """Auto-initialize the database if the task table is missing."""
    db = get_db()
    try:
        db.execute('SELECT 1 FROM task LIMIT 1').fetchone()
    except sqlite3.OperationalError:
        init_db()
    # Lower-level init-db ensures commit, nothing else needed

@app.route('/')
def index():
    filter_status = request.args.get('filter', 'all')
    sort_key = request.args.get('sort', 'due_date')
    db = get_db()
    query = 'SELECT * FROM task'
    conditions = []
    if filter_status == 'active':
        conditions.append('complete = 0')
    elif filter_status == 'completed':
        conditions.append('complete = 1')
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    if sort_key in ('due_date', 'created_at', 'priority'):
        query += f' ORDER BY {sort_key}'
    tasks = db.execute(query).fetchall()
    return render_template('index.html', tasks=tasks, filter_status=filter_status, sort_key=sort_key)

@app.route('/add', methods=('POST',))
def add():
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '')
    priority = request.form.get('priority', 'Medium')
    if not title:
        flash('Title is required.', 'danger')
    else:
        db = get_db()
        db.execute(
            'INSERT INTO task (title, due_date, priority) VALUES (?, ?, ?)',
            (title, due_date or None, priority)
        )
        db.commit()
        flash('Task added!', 'success')
    return redirect(url_for('index'))

@app.route('/<int:task_id>/toggle', methods=('POST',))
def toggle(task_id):
    db = get_db()
    task = db.execute('SELECT complete FROM task WHERE id = ?', (task_id,)).fetchone()
    if task:
        new_status = 0 if task['complete'] else 1
        db.execute('UPDATE task SET complete = ? WHERE id = ?', (new_status, task_id))
        db.commit()
        flash('Task status updated.', 'success')
    else:
        flash('Task not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/<int:task_id>/delete', methods=('POST',))
def delete(task_id):
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (task_id,))
    db.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/<int:task_id>/edit', methods=('GET', 'POST'))
def edit(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        due_date = request.form.get('due_date', '')
        priority = request.form.get('priority', 'Medium')
        if not title:
            flash('Title is required.', 'danger')
        else:
            db.execute(
                'UPDATE task SET title = ?, due_date = ?, priority = ? WHERE id = ?',
                (title, due_date or None, priority, task_id)
            )
            db.commit()
            flash('Task updated.', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)