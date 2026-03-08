from flask import Blueprint, render_template, session, redirect, url_for, flash
from database import Recruiter, Job

recruiters_bp = Blueprint('recruiters', __name__, url_prefix='/recruiter')

@recruiters_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'recruiter':
        flash('Please login as a recruiter', 'danger')
        return redirect(url_for('auth.login'))

    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    if not recruiter:
        flash('Recruiter profile not found. Please complete your profile.', 'warning')
        return redirect(url_for('recruiters.profile'))

    jobs = Job.query.filter_by(recruiter_id=recruiter.id).all()

    return render_template('recruiter-dashboard.html', jobs=jobs, name=session.get('name'))
