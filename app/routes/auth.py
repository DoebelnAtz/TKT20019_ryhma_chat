import secrets
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.utils.auth import negate_login_required
from app.db import db
from app.utils.users import create_user, get_user_by_username
from app.utils.errors import handle_errors

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=('GET', 'POST'))
@handle_errors
@negate_login_required
def signup():
    error = request.args.get('error')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        elif len(password) > 100:
            error = 'Password must be less than 100 characters long.'
        elif get_user_by_username(username):
            error = 'Username is already taken.'

        if error is None:
            create_user(username, password)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.signup', error=error))
    return render_template('auth/signup.html', error=error)


@auth_bp.route('/login', methods=('GET', 'POST'))
@handle_errors
@negate_login_required
def login():
    error = request.args.get('error')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        error = None
        if user is None:
            # Generally considered a bad practice to leak information about
            # why login failed, but for this app I'll consider it a feature.
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        if error is None:
            session['username'] = user.username
            session['user_id'] = user.id
            session['csrf_token'] = secrets.token_hex(16)
            return redirect(url_for('root.index'))
        else:
            return redirect(url_for('auth.login', error=error))
    return render_template('auth/login.html', error=error)


@auth_bp.route('/logout')
@handle_errors
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
