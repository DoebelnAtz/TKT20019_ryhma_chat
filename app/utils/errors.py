from functools import wraps
from flask import redirect, url_for, flash


class HTTPError(Exception):
    status = 500

    def __init__(self, message, status=None):
        super().__init__()
        self.message = message
        if status is not None:
            self.status = status

    def to_string(self):
        return f"{self.status} {self.message}"


def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            if e.status == 401:
                flash("You must be logged in to do that.")
                return redirect(url_for('auth.login'))
            if e.status == 404:
                flash("Not found.")
                return redirect(url_for('errors.not_found'))
            flash(e.to_string())
            return redirect(url_for('errors.error', error_message=e.to_string()))
        except Exception:
            flash("Something went wrong.")
            return redirect(url_for('errors.error', error_message="Something went wrong"))
    return decorated_function
