import traceback
from functools import wraps
from flask_socketio import emit
from flask import redirect, url_for
from app.utils.logger import Logger
logger = Logger(__name__)


class HTTPError(Exception):
    status = 500

    def __init__(self, message, status=None):
        super().__init__()
        self.message = message
        if status is not None:
            self.status = status

    def _to_string(self):
        return f"{self.status} {self.message}"

    def __str__(self):
        return self._to_string()


def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            logger.error(str(e), traceback.format_exc())
            if e.status == 403:
                return redirect(url_for('errors.forbidden'))
            if e.status == 404:
                return redirect(url_for('errors.not_found'))
            return redirect(url_for('errors.error', error_message=str(e), status=e.status))
        except Exception as e:
            logger.error(str(e), traceback.format_exc())
            return redirect(url_for('errors.error',
                                    error_message="Something went wrong",
                                    status=500))
    return decorated_function


def handle_socket_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            logger.error(str(e), traceback.format_exc())
            if e.status == 500:
                emit("error", "Something went wrong.", broadcast=True)
            else:
                emit("error", str(e), broadcast=True)
            return None
        except Exception as e:
            logger.error(str(e), traceback.format_exc())
            emit("error", "Something went wrong.", broadcast=True)
            return None
    return decorated_function
