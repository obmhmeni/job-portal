from flask import Blueprint, request, jsonify, session, url_for
from database import db, Job, Recruiter
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session or session.get('role') != 'recruiter':
        return jsonify({'success': False, 'error': 'Unauthorized - Please login as recruiter'}), 401

    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    if not recruiter:
        return jsonify({'success': False, 'error': 'Recruiter profile not found'}), 404

    if request.method == 'GET':
        return render_template('post-job.html')

    # POST request
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        # Basic validation
        if not data.get('job_name') or not data.get('description') or not data.get('required_skills'):
            return jsonify({'success': False, 'error': 'Job name, description and skills are required'}), 400

        # Description word limit
        words = len(data['description'].split())
        if words > 100:
            return jsonify({'success': False, 'error': 'Description exceeds 100 words'}), 400

        new_job = Job(
            recruiter_id=recruiter.id,
            job_name=data['job_name'],
            description=data['description'],
            location=data.get('location', ''),
            required_experience=data.get('required_experience', ''),
            required_qualification=data.get('required_qualification', ''),
            required_skills=data.get('required_skills', ''),  # <-- Yeh add kiya
            num_people=data.get('num_people', 1),
            salary=data.get('salary', ''),
            company_info=data.get('company_info', ''),
            created_at=datetime.utcnow()
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Job posted successfully!',
            'job_id': new_job.id
        })

    except Exception as e:
        db.session.rollback()
        print(f"Job post error: {str(e)}")  # Yeh Render logs mein dikhega
        return jsonify({'success': False, 'error': 'Server error while saving job'}), 500
