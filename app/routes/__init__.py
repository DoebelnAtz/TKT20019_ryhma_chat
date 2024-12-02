from flask import Blueprint, redirect, render_template, session, url_for
from app.utils.auth import login_required
from app.utils.errors import handle_errors
from app.utils.groups import get_user_groups, get_user_invites


root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET'])
@login_required
@handle_errors
def index():
    user_groups = get_user_groups()
    user_invites = get_user_invites()
    return render_template('index.html', groups=user_groups, invites=user_invites)


@root_bp.route('/toggle_theme', methods=['POST'])
@login_required
@handle_errors
def toggle_theme():
    session['theme'] = 'dark' if session.get('theme') == 'light' else 'light'
    return redirect(url_for('root.index'))
