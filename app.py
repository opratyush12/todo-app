from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# File to store tasks
TODO_FILE = '/data/tasks.json'

# Ensure data directory exists
os.makedirs('/data', exist_ok=True)

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks = load_tasks()
        tasks.append({'id': len(tasks) + 1, 'task': task, 'completed': False})
        save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    # Reassign IDs
    for i, task in enumerate(tasks, 1):
        task['id'] = i
    save_tasks(tasks)
    return redirect('/')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)