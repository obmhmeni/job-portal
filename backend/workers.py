from flask import Blueprint, render_template, session, redirect, url_for
from database import Worker

workers_bp = Blueprint('workers', __name__, url_prefix='/worker')

@workers_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'worker':
        return redirect(url_for('auth.login'))
    
    worker = Worker.query.filter_by(user_id=session['user_id']).first()
    return render_template('worker-dashboard.html', 
                           name=session.get('name'), 
                           worker=worker)
