from functools import wraps
from flask import session, redirect, url_for, request
from app.utils.errors import HTTPError


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def negate_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method != 'GET':
            return f(*args, **kwargs)
        if session.get('user_id') is not None:
            return redirect(url_for('root.index'))
        return f(*args, **kwargs)
    return decorated_function


def csrf_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'GET':
            return f(*args, **kwargs)
        if not request.form.get('csrf_token'):
            raise HTTPError('CSRF token is missing.', 400)
        if session.get('csrf_token') != request.form['csrf_token']:
            raise HTTPError('Invalid CSRF token.', 403)
        return f(*args, **kwargs)
    return decorated_function
