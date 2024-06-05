from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import click  

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        with app.open_resource('setup.sql', mode='r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    else:
        print("Failed to initialize database")

@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logins WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user['password_hash'], password):
                session.clear()
                session['user_id'] = user['id']
                session['user_name'] = user['email']
                flash('Login successful!')
                return redirect(url_for('jobs'))
            else:
                flash('Invalid email or password!')
        else:
            flash('Database connection error!')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or not email or not password or not confirm_password:
            flash('All fields are required!')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO register (name, email, password_hash) VALUES (?, ?, ?)",
                               (name, email, hashed_password))
                cursor.execute("INSERT INTO logins (email, password_hash) VALUES (?, ?)",
                               (email, hashed_password))
                conn.commit()
                cursor.execute("SELECT id FROM logins WHERE email = ?", (email,))
                user = cursor.fetchone()
                session.clear()
                session['user_id'] = user['id']
                session['user_name'] = email
                flash('Registration successful! You are now logged in.')
                return redirect(url_for('jobs'))
            except sqlite3.IntegrityError:
                flash('Email already exists!')
            finally:
                conn.close()
        else:
            flash('Database connection error!')
        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']
        salary = request.form['salary']

        conn = get_db_connection()
        if conn:
            try:
                conn.execute(
                    "INSERT INTO jobs (title, faculty, interview_details, news) VALUES (?, ?, ?, ?, ?)",
                    ("title", "faculty", "interview_details", "news")
                )
                conn.commit()
            except sqlite3.Error as e:
                flash(f"An error occurred: {e.args[0]}")
            finally:
                conn.close()

    conn = get_db_connection()
    if conn:
        jobs = conn.execute("SELECT * FROM jobs").fetchall()
        conn.close()
        return render_template('jobs.html', jobs=jobs)
    else:
        flash('Database connection error!')
        return redirect(url_for('home'))

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/resume")
def resume():
    return render_template('resume.html')

@app.route('/companyname')
def companyname():
    return render_template('companyname.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first!')
        return redirect(url_for('login'))

    return render_template('dashboard.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
