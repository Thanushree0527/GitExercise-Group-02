from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
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

        print(f"Received: name={name}, email={email}, password={password}, confirm_password={confirm_password}")

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
                print('User registered and logged in successfully')  
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
        faculty = request.form['faculty']
        interview_details = request.form['interview_details']
        news = request.form['news']

        conn = get_db_connection()
        if conn:
            try:
                conn.execute(
                    "INSERT INTO jobs (title, faculty, interview_details, news) VALUES (?, ?, ?, ?)",
                    (title, faculty, interview_details, news)
                )
                conn.commit()
                flash('Job added successfully!')
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

@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = get_db_connection()
    if conn:
        try:
            conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            conn.commit()
            flash('Job deleted successfully!')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        flash('Database connection error!')

    return redirect(url_for('jobs'))

@app.route('/companyname')
def companyname():
    conn = get_db_connection()
    if conn:
        companies = conn.execute("SELECT * FROM companies").fetchall()
        conn.close()
        return render_template('companyname.html', companies=companies)
    else:
        flash('Database connection error!')
        return redirect(url_for('home'))

@app.route('/add_company', methods=['POST'])
def add_company():
    if request.method == 'POST':
        faculty = request.form['faculty']
        company_title = request.form['company_title']
        company_address = request.form['company_address']
        
        print(f"Received: faculty={faculty}, company_title={company_title}, company_address={company_address}")

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO companies (faculty, company_title, address) VALUES (?, ?, ?)",
                               (faculty, company_title, company_address))
                conn.commit()
                flash('Company added successfully!')
                print("Company added to database.")
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                print(f"Database error: {e}")
            finally:
                conn.close()
        else:
            flash('Database connection error!')

    return redirect(url_for('companyname'))

@app.route('/delete_company', methods=['POST'])
def delete_company():
    company_id = request.form['company_id']
    conn = get_db_connection()
    if conn:
        try:
            conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
            conn.commit()
            flash('Company deleted successfully!')
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        flash('Database connection error!')

    return redirect(url_for('companyname'))

@app.route('/chat_box')
def chat_assessment_form():
    return render_template('chat.html')

@app.route('/submit_chat', methods=['POST'])
def submit_chat():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        mobile = request.form['mobile']
        nationality = request.form['nationality']
        interested_job = request.form['interestedJob']
        inquiries = request.form['inquiries']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO chat_box (first_name, last_name, email, mobile, nationality, interested_job, inquiries) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                               (first_name, last_name, email, mobile, nationality, interested_job, inquiries))
                conn.commit()
                conn.close()
                flash('Chat details submitted successfully!')
                return redirect(url_for('chat_assessment_form'))  # Corrected redirection
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                conn.rollback()
                conn.close()
        else:
            flash('Database connection error!')
        
    return redirect(url_for('chat_assessment_form'))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        admission_office_contact = request.form['admission_office_contact']
        address = request.form['address']
        business_hours = request.form['business_hours']

        conn = get_db_connection()
        if conn:
            try:
                conn.execute(
                    "INSERT INTO contact (email, admission_office_contact, address, business_hours) VALUES (?, ?, ?, ?)",
                    (email, admission_office_contact, address, business_hours)
                )
                conn.commit()
                flash('Contact information added successfully!')
            except sqlite3.Error as e:
                flash(f"An error occurred: {e.args[0]}")
            finally:
                conn.close()

    conn = get_db_connection()
    if conn:
        contacts = conn.execute("SELECT * FROM contact").fetchall()
        conn.close()
        return render_template('contact.html', contacts=contacts)
    else:
        flash('Database connection error!')
        return redirect(url_for('home'))

@app.route('/delete_contact/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Delete the contact with the specified ID
            cursor.execute("DELETE FROM contact WHERE id = ?", (contact_id,))
            conn.commit()
            flash('Contact deleted successfully!')
        except sqlite3.Error as e:
            flash(f"An error occurred while deleting contact: {e}")
        finally:
            conn.close()
    else:
        flash('Database connection error!')
    
    return redirect(url_for('contact'))

@app.route('/submit_resume', methods=['POST'])
def submit_resume():
    try:
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        contact_information = request.form['contact_information']
        address = request.form['address']
        academic_qualification = request.form['academic_qualification']
        expected_graduation_date = request.form['expected_graduation_date']
        gpa = request.form['gpa']
        job_title = request.form['job_title']
        company_name = request.form['company_name']
        job_address = request.form['job_address']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        responsibilities_and_achievements = request.form['responsibilities_and_achievements']
        objective_or_summary = request.form['objective_or_summary']
        skills = request.form['skills']
        extracurricular_activities = request.form['extracurricular_activities']
        references_list = request.form['references_list']
        interested_faculty = request.form['interested_faculty']
        interested_job = request.form['interested_job']
        interested_company = request.form['interested_company']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO resume (
                        name, email, contact_information, address,
                        academic_qualification, expected_graduation_date, gpa,
                        job_title, company_name, job_address, start_date, end_date,
                        responsibilities_and_achievements, objective_or_summary,
                        skills, extracurricular_activities, references_list,
                        interested_faculty, interested_job, interested_company
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, email, contact_information, address,
                    academic_qualification, expected_graduation_date, gpa,
                    job_title, company_name, job_address, start_date, end_date,
                    responsibilities_and_achievements, objective_or_summary,
                    skills, extracurricular_activities, references_list,
                    interested_faculty, interested_job, interested_company
                ))
                conn.commit()
                flash('Resume submitted successfully!')
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                conn.rollback()
            finally:
                conn.close()
        else:
            flash('Database connection error!')
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while submitting the resume.')

    return redirect(url_for('thankyou'))

@app.route('/faq')
def faq():
    conn = get_db_connection()
    if conn:
        faqs = conn.execute("SELECT * FROM faq_questions").fetchall()
        conn.close()
        return render_template('faq.html', faqs=faqs)
    else:
        flash('Database connection error!')
        return redirect(url_for('home'))

@app.route('/add_faq', methods=['POST'])
def add_faq():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO faq_questions (question, answer) VALUES (?, ?)", (question, answer))
                conn.commit()
                flash('FAQ added successfully!')
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            flash('Database connection error!')

    return redirect(url_for('faq'))

@app.route('/delete_faq/<int:faq_id>', methods=['POST'])
def delete_faq(faq_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM faq_questions WHERE id = ?", (faq_id,))
            conn.commit()
            flash('FAQ deleted successfully!')
        except sqlite3.Error as e:
            flash(f"An error occurred while deleting FAQ: {e}")
        finally:
            conn.close()
    else:
        flash('Database connection error!')

    return redirect(url_for('faq'))

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

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

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', 'next-gen vision.wav')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
