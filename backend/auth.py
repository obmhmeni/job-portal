from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from database import db, User, Worker, Recruiter, Log
from werkzeug.security import generate_password_hash, check_password_hash
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    temp_role = session.get('temp_role', 'worker')

    if request.method == 'GET':
        return render_template('signup.html', role=temp_role)

    # POST
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'No data received'}), 400

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    state = data.get('state')

    if not all([name, email, phone, password, state]):
        return jsonify({'success': False, 'error': 'All fields required'}), 400

    # Duplicate check
    if User.query.filter((User.email == email) | (User.phone == phone)).first():
        return jsonify({'success': False, 'error': 'Email or phone already registered'}), 409

    user = User(name=name, email=email, phone=phone, state=state, role=temp_role)
    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    if temp_role == 'worker':
        db.session.add(Worker(user_id=user.id))
    else:
        db.session.add(Recruiter(user_id=user.id))

    db.session.commit()

    session.pop('temp_role', None)

    return jsonify({
        'success': True,
        'redirect': url_for('auth.login')
    })

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

            # Optional log
            try:
                log = Log(user_id=user.id, action='login', details=json.dumps({'method': data.get('email')}))
                db.session.add(log)
                db.session.commit()
            except:
                db.session.rollback()

            # Direct dashboard paths (main.py ke routes)
            if user.role == 'recruiter':
                redirect_url = '/recruiter-dashboard'
            else:
                redirect_url = '/worker-dashboard'

            return jsonify({
                'success': True,
                'redirect': redirect_url,
                'name': user.name,
                'role': user.role
            })

        return jsonify({'error': 'Invalid credentials'})

    return render_template('login.html')
