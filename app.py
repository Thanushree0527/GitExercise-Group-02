from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config = ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db =SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))

    def __iniit__(self,email,password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode(utf-8)),



@app.route('/')
def home():
    return ("Hello from Flask!")

if __name__ == '__main__':
    app.run(debug=True)
