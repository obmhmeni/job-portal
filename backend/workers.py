from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from database import db, Worker, Log
import json

workers_bp = Blueprint('workers', __name__)

@workers_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('role') != 'worker':
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    worker = Worker.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        data = request.json
        worker.address = data['address']
        worker.qualification = data['qualification']
        worker.experience_years = data['experience_years']
        worker.skills = data['skills']  # Comma-separated
        db.session.commit()
        log = Log(user_id=user_id, action='update_profile', details=json.dumps(data))
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('worker-profile.html', worker=worker)  # + 500 words filler
