from flask import Blueprint, request, render_template, jsonify, session
from database import db, User, Log
import json

auth_bp = Blueprint('auth', __name__)

# ... baaki imports same ...

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

            try:
                log = Log(user_id=user.id, action='login', details=json.dumps({'method': data.get('email')}))
                db.session.add(log)
                db.session.commit()
            except:
                db.session.rollback()

            # Simple redirect URLs (main.py ke direct routes)
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


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    temp_role = session.get('temp_role', 'worker')
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data'}), 400

        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            state=data['state'],
            role=temp_role
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.flush()

        if temp_role == 'worker':
            db.session.add(Worker(user_id=user.id))
        else:
            db.session.add(Recruiter(user_id=user.id))

        db.session.commit()

        session.pop('temp_role', None)
        return jsonify({'success': True, 'redirect': url_for('auth.login')})

    return render_template('signup.html', role=temp_role)



