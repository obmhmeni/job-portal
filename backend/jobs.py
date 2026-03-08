from flask import Blueprint, request, jsonify, session, render_template, flash, url_for, redirect
from database import db, Job, Recruiter
from datetime import datetime
import json

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    # Auth check
    if 'user_id' not in session or session.get('role') != 'recruiter':
        flash('Only recruiters can post jobs. Please login.', 'danger')
        return redirect(url_for('auth.login'))

    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    if not recruiter:
        flash('Recruiter profile not found. Please complete your profile.', 'warning')
        return redirect(url_for('recruiters.profile'))

    if request.method == 'GET':
        return render_template('post-job.html')

    # POST request (AJAX se aa raha hai)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        # Required fields check
        required_fields = ['job_name', 'description', 'location', 'salary', 'required_skills']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400

        # Description word limit (100 words)
        words = len(data['description'].split())
        if words > 100:
            return jsonify({'success': False, 'error': 'Description cannot exceed 100 words'}), 400

        # Create new job
        new_job = Job(
            recruiter_id=recruiter.id,
            job_name=data['job_name'].strip(),
            description=data['description'].strip(),
            location=data.get('location', '').strip(),
            salary=data.get('salary', '').strip(),
            required_experience=data.get('required_experience', '').strip(),
            required_qualification=data.get('required_qualification', '').strip(),
            required_skills=data['required_skills'].strip(),  # comma separated
            num_people=int(data.get('num_people', 1)),
            company_info=data.get('company_info', '').strip(),
            created_at=datetime.utcnow()
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Job posted successfully!',
            'redirect': url_for('recruiter_dashboard')  # wapas dashboard pe
        })

    except ValueError as ve:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Invalid number format for people needed'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Job post error: {str(e)}")  # Render logs mein dikhega
        return jsonify({'success': False, 'error': 'Server error while posting job. Please try again.'}), 500


@jobs_bp.route('/all-jobs')
def all_jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)
