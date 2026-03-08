from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from database import db, Recruiter, Log
import json

recruiters_bp = Blueprint('recruiters', __name__)

@recruiters_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('role') != 'recruiter':
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    recruiter = Recruiter.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        data = request.json
        recruiter.company_name = data['company_name']
        recruiter.company_address = data['company_address']
        db.session.commit()
        log = Log(user_id=user_id, action='update_profile', details=json.dumps(data))
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('recruiter-profile.html', recruiter=recruiter)  # Post job button
