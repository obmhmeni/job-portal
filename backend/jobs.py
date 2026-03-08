from flask import Blueprint, request, render_template, jsonify, session
from database import db, Job, Worker, Recruiter
from sqlalchemy import or_
import json

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if session.get('role') != 'recruiter':
        return jsonify({'error': 'Unauthorized'})
    recruiter = Recruiter.query.filter_by(user_id=session['user_id']).first()
    if request.method == 'POST':
        data = request.json
        if len(data['description'].split()) > 100:  # 100 words limit
            return jsonify({'error': 'Description too long'})
        job = Job(
            recruiter_id=recruiter.id, job_name=data['job_name'], description=data['description'],
            location=data['location'], required_experience=data['experience'],
            required_qualification=data['qualification'], num_people=data['num_people'],
            salary=data['salary'], company_info=data['company_info']
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('post-job.html')

@jobs_bp.route('/search-workers', methods=['GET'])
def search_workers():
    if session.get('role') != 'recruiter':
        return jsonify({'error': 'Unauthorized'})
    skills = request.args.get('skills', '').split(',')
    workers = Worker.query.join(Worker.user).filter(
        or_(*[Worker.skills.like(f'%{s.strip()}%') for s in skills if s.strip()])
    ).all()
    results = []
    for w in workers:
        results.append({
            'name': w.user.name, 'email': w.user.email, 'phone': w.user.phone,
            'skills': w.skills, 'qualification': w.qualification
        })
    return jsonify({'workers': results})

@jobs_bp.route('/all-jobs')
def all_jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)
