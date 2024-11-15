from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username:
            flash('Username is required.')
        elif not password:
            flash('Password is required.')
        else:
            existing_user = db.session.query(User).filter(User.username == username).first()
            if existing_user:
                flash('Username is already taken.')
            else:
                new_user = User(username=username, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.username == username).first()
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
            return redirect(url_for('root.index'))
        else:
            flash(error)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))