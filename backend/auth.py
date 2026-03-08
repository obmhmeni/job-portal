from flask import Blueprint, request, render_template, jsonify, session
from database import db, User, Log
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email_or_phone = data.get('email')
        password = data.get('password')

        user = User.query.filter(
            db.or_(User.email == email_or_phone, User.phone == email_or_phone)
        ).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name

            # Optional logging
            try:
                log = Log(user_id=user.id, action='login', details=json.dumps({'method': email_or_phone}))
                db.session.add(log)
                db.session.commit()
            except:
                db.session.rollback()  # ignore log error

            # Role ke hisaab se redirect URL decide karo
            if user.role == 'recruiter':
                redirect_url = url_for('recruiter_dashboard')   # → /recruiter/dashboard
            else:
                redirect_url = url_for('worker_dashboard')      # → /worker/dashboard

            return jsonify({
                'success': True,
                'redirect': redirect_url,
                'name': user.name,
                'role': user.role
            })

        return jsonify({'error': 'Invalid credentials'})

    return render_template('login.html')
