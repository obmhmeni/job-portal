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

# Blueprints register kar rahe hain prefix ke saath
app.register_blueprint(auth_bp)
app.register_blueprint(workers_bp, url_prefix='/worker')
app.register_blueprint(recruiters_bp, url_prefix='/recruiter')
app.register_blueprint(jobs_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user=session.get('name'), role=session.get('role'))
    return render_template('index.html')

# Dashboard routes ko main.py se hata diya – ab blueprint mein honge
# Yeh file sirf root aur blueprints ko handle karegi

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
