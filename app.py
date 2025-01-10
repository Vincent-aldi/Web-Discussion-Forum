from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_threads = []
users = {}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', threads=data_threads, username=session['username'])

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if 0 <= thread_id < len(data_threads):
        return render_template('thread.html', thread=data_threads[thread_id], username=session['username'])
    return "Thread not found", 404

@app.route('/create', methods=['GET', 'POST'])
def create_thread():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        data_threads.append({'title': title, 'content': content, 'comments': []})
        return redirect(url_for('index'))
    return render_template('create_thread.html', username=session['username'])

@app.route('/thread/<int:thread_id>/comment', methods=['POST'])
def comment(thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if 0 <= thread_id < len(data_threads):
        comment = request.form['comment']
        data_threads[thread_id]['comments'].append({'username': session['username'], 'comment': comment})
        return redirect(url_for('thread', thread_id=thread_id))
    return "Thread not found", 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists", 400
        users[username] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials", 400
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
