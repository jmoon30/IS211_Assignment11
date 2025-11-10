from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global list to store to-do items
# Each item is a dict: {"task": ..., "email": ..., "priority": ...}
todo_items = []


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error')
    return render_template('index.html', items=todo_items, error=error)


@app.route('/submit', methods=['POST'])
def submit_item():
    global todo_items

    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '').strip()

    # Basic validation

    # require all fields
    if not task or not email or not priority:
        return redirect(url_for('index', error='All fields are required.'))

    # very simple email check (matches assignment expectations)
    if '@' not in email or '.' not in email.split('@')[-1]:
        return redirect(url_for('index', error='Please enter a valid email address.'))

    # validate priority
    allowed_priorities = ['Low', 'Medium', 'High']
    if priority not in allowed_priorities:
        return redirect(url_for('index', error='Invalid priority selected.'))

    # If valid, add to global list
    todo_items.append({
        'task': task,
        'email': email,
        'priority': priority
    })

    # Redirect back to main page
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_items():
    global todo_items
    todo_items = []  # reset to empty list
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Access via http://localhost:5000
    app.run(debug=True)
