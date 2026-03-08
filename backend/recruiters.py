from flask import Blueprint, render_template, session, redirect, url_for
from database import Recruiter, Job

recruiters_bp = Blueprint('recruiters', __name__, url_prefix='/recruiter')

@recruiters_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'recruiter':
        return redirect(url_for('auth.login'))
    
    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    jobs = Job.query.filter_by(recruiter_id=recruiter.id).all() if recruiter else []
    
    return render_template('recruiter-dashboard.html', 
                           name=session.get('name'), 
                           jobs=jobs)
