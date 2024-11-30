from flask import Blueprint, render_template, session
from sqlalchemy import text
from app.utils.auth import login_required
from app.utils.errors import handle_errors
from app.utils.groups import get_user_groups, get_user_invites
from app import db

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
@login_required
@handle_errors
def index():
    user_groups = get_user_groups()
    user_invites = get_user_invites()
    return render_template('index.html', groups=user_groups, invites=user_invites)
