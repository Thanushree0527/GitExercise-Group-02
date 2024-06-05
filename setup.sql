-- Drop the existing logins and register tables if they exist 
DROP TABLE IF EXISTS logins; 
DROP TABLE IF EXISTS register; 
DROP TABLE IF EXISTS jobs; 
DROP TABLE IF EXISTS chat_assessments; 
 
-- Create a new logins table to store login details 
CREATE TABLE IF NOT EXISTS logins ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT UNIQUE NOT NULL, 
    password_hash TEXT NOT NULL 
); 
 
-- Create a new register table to store registration details 
CREATE TABLE IF NOT EXISTS register ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    email TEXT UNIQUE NOT NULL, 
    password_hash TEXT NOT NULL 
); 
 
CREATE TABLE IF NOT EXISTS jobs ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT NOT NULL, 
    faculty TEXT NOT NULL, 
    interview_details TEXT NOT NULL, 
    news TEXT 
); 
 
-- Create a new chat_assessments table to store chat assessment details 
CREATE TABLE IF NOT EXISTS chat_assessments ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    mobile TEXT NOT NULL, 
    nationality TEXT NOT NULL, 
    interested_job TEXT NOT NULL, 
    inquiries TEXT NOT NULL 
); 