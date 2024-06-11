-- Drop the existing tables if they exist
DROP TABLE IF EXISTS logins;
DROP TABLE IF EXISTS register;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS chat_box;
DROP TABLE IF EXISTS contact;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS resume;
DROP TABLE IF EXISTS faq_questions;

-- Create the logins table
CREATE TABLE IF NOT EXISTS logins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Create the register table
CREATE TABLE IF NOT EXISTS register (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Create the jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    faculty TEXT NOT NULL,
    interview_details TEXT NOT NULL,
    news TEXT
);

-- Create the chat_assessments table
CREATE TABLE IF NOT EXISTS chat_box (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile TEXT NOT NULL,
    nationality TEXT NOT NULL,
    interested_job TEXT NOT NULL,
    inquiries TEXT NOT NULL
);

-- Create the contact table
CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    admission_office_contact TEXT NOT NULL,
    address TEXT NOT NULL,
    business_hours TEXT
);

-- Create the companies table
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty TEXT NOT NULL,
    company_title TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE resume (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    contact_information TEXT NOT NULL,
    address TEXT NOT NULL,
    academic_qualification TEXT NOT NULL,
    expected_graduation_date TEXT NOT NULL,
    gpa TEXT NOT NULL,
    job_title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    job_address TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    responsibilities_and_achievements TEXT NOT NULL,
    objective_or_summary TEXT NOT NULL,
    skills TEXT NOT NULL,
    extracurricular_activities TEXT NOT NULL,
    references_list TEXT NOT NULL,
    interested_faculty TEXT NOT NULL,
    interested_job TEXT NOT NULL,
    interested_company TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS faq_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);