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
    # Temp role role-select se aaya hai
    temp_role = session.get('temp_role', 'worker')

    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        try:
            user = User(
                name=data['name'].strip(),
                email=data['email'].strip(),
                phone=data['phone'].strip(),
                state=data['state'].strip(),
                role=temp_role
            )
            user.set_password(data['password'])

            db.session.add(user)
            db.session.flush()  # user.id mil jaye

            if temp_role == 'worker':
                worker = Worker(user_id=user.id)
                db.session.add(worker)
            else:
                recruiter = Recruiter(user_id=user.id)
                db.session.add(recruiter)

            db.session.commit()

            session.pop('temp_role', None)

            return jsonify({
                'success': True,
                'redirect': url_for('auth.login')
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    # GET request - page dikhana
    return render_template('signup.html', role=temp_role)
