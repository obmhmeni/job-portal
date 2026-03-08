from flask import Blueprint, render_template, session, redirect, url_for, flash
from database import Worker

workers_bp = Blueprint('workers', __name__, url_prefix='/worker')

@workers_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'worker':
        flash('Please login as a worker', 'danger')
        return redirect(url_for('auth.login'))

    worker = Worker.query.filter_by(user_id=session['user_id']).first()
    if not worker:
        flash('Worker profile not found. Please complete your profile.', 'warning')
        return redirect(url_for('workers.profile'))  # agar profile route hai toh

    return render_template('worker-dashboard.html', worker=worker, name=session.get('name'))
