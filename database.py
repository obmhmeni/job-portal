from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='worker')  # 'worker' or 'recruiter'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.Text)
    qualification = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    skills = db.Column(db.Text)  # "Python, Welding, Driving"
    user = db.relationship('User', backref='worker')

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100))
    company_address = db.Column(db.Text)
    user = db.relationship('User', backref='recruiter')

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    job_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)  # 100 words limit backend mein
    location = db.Column(db.String(100))
    required_experience = db.Column(db.String(50))
    required_qualification = db.Column(db.String(100))
    num_people = db.Column(db.Integer)
    salary = db.Column(db.String(50))
    company_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recruiter = db.relationship('Recruiter', backref='jobs')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100))  # 'signup', 'login', 'update_profile', 'post_job'
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
