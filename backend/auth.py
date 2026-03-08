from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from database import db, User, Log
import json
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/role-select', methods=['GET', 'POST'])
def role_select():
    if request.method == 'POST':
        role = request.json.get('role')
        if role in ['worker', 'recruiter']:
            session['temp_role'] = role
            return jsonify({'redirect': url_for('auth.signup')})
    return render_template('role-select.html')  # Big fonts page + policy

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    temp_role = session.get('temp_role', 'worker')
    if request.method == 'POST':
        data = request.json
        user = User(
            name=data['name'], email=data['email'], phone=data['phone'],
            state=data['state'], role=temp_role
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        if temp_role == 'worker':
            from database import Worker
            db.session.add(Worker(user_id=user.id))
        else:
            from database import Recruiter
            db.session.add(Recruiter(user_id=user.id))
        log = Log(user_id=user.id, action='signup', details=json.dumps(data))
        db.session.add(log)
        db.session.commit()
        del session['temp_role']
        flash('Signup successful! Please login.')
        return jsonify({'redirect': url_for('auth.login')})
    return render_template('signup.html', role=temp_role)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        user = User.query.filter(
            db.or_(User.email == data.get('email'), User.phone == data.get('phone'))
        ).first()
        if user and user.check_password(data.get('password')):
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            log = Log(user_id=user.id, action='login', details=json.dumps({'method': data.get('email') or data.get('phone')}))
            db.session.add(log)
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('index'), 'name': user.name})
        return jsonify({'error': 'Invalid credentials'})
    return render_template('login.html')
