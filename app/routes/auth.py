import secrets
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import db
from app.utils.users import create_user, get_user_by_username
from app.utils.errors import handle_errors

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=('GET', 'POST'))
@handle_errors
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Username is required.')
        elif not password:
            flash('Password is required.')
        else:
            existing_user = get_user_by_username(username)
            if existing_user:
                flash('Username is already taken.')
            else:
                create_user(username, password)
                db.session.commit()
                return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
@handle_errors
def login():
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
            flash(error)
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@handle_errors
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
