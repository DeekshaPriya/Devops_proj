from flask import Flask, request, session, redirect, url_for, render_template, send_from_directory
import redis
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'minidrive-secret-key'

r = redis.Redis(host='redis', port=6379, decode_responses=True)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Auth ──────────────────────────────────────────────
USERS = {'admin': 'password123', 'student': 'university'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if USERS.get(u) == p:
            session['user'] = u
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── Dashboard ─────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    files = []
    keys = r.keys(f'file:{user}:*')
    for key in keys:
        meta = r.hgetall(key)
        files.append(meta)
    total = sum(int(f.get('size', 0)) for f in files)
    return render_template('dashboard.html', files=files, user=user, total=total)

# ── Upload ────────────────────────────────────────────
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, user, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        r.hset(f'file:{user}:{filename}', mapping={
            'filename': filename,
            'size': os.path.getsize(filepath),
            'uploaded': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'owner': user
        })
    return redirect(url_for('dashboard'))

# ── Delete ────────────────────────────────────────────
@app.route('/delete/<filename>')
def delete(filename):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    filepath = os.path.join(UPLOAD_FOLDER, user, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    r.delete(f'file:{user}:{filename}')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)