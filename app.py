from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('job_application.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create tables in the database
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        profile_picture TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_id INTEGER NOT NULL,
                        skill TEXT NOT NULL,
                        FOREIGN KEY(profile_id) REFERENCES profiles(id)
                    )''')
    conn.commit()
    conn.close()

# Create tables when the app starts
create_tables()

# Route to display the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle profile picture upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('index'))
    return render_template('upload.html')

# Route to handle profile editing
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form.getlist('skills')
        languages = request.form.getlist('languages')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
        profile_id = cursor.lastrowid
        for skill in skills:
            cursor.execute("INSERT INTO skills (profile_id, skill) VALUES (?, ?)", (profile_id, skill))
        conn.commit()
        conn.close()
        flash('Profile successfully updated')
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)