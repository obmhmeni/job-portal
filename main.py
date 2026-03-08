from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
from database import db
from backend.auth import auth_bp
from backend.workers import workers_bp
from backend.recruiters import recruiters_bp
from backend.jobs import jobs_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(workers_bp, url_prefix='/worker')
app.register_blueprint(recruiters_bp, url_prefix='/recruiter')
app.register_blueprint(jobs_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user=session.get('name'), role=session.get('role'))
    return render_template('index.html')


# workers_bp aur recruiters_bp ko register karte waqt url_prefix mat do dashboard ke liye
# Ya fir seedha main.py mein routes define karo

@app.route('/worker-dashboard')
def worker_dashboard():
    if 'user_id' not in session or session.get('role') != 'worker':
        return redirect(url_for('auth.login'))
    worker = Worker.query.filter_by(user_id=session['user_id']).first()
    return render_template('worker-dashboard.html', name=session.get('name'), worker=worker)

@app.route('/recruiter-dashboard')
def recruiter_dashboard():
    if 'user_id' not in session or session.get('role') != 'recruiter':
        return redirect(url_for('auth.login'))
    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    jobs = Job.query.filter_by(recruiter_id=recruiter.id).all() if recruiter else []
    return render_template('recruiter-dashboard.html', name=session.get('name'), jobs=jobs)

# Create tables (dev only)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
