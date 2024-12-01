from flask import Blueprint, render_template, request

errors_bp = Blueprint('errors', __name__)


@errors_bp.route('/not_found')
def not_found():
    return render_template('errors/not_found.html'), 404


@errors_bp.route('/error')
def error():
    error_message = request.args.get('error_message')
    status = request.args.get('status')
    return render_template('errors/error.html', error_message=error_message, status=status), status
