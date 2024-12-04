from flask import Blueprint, render_template
from app.utils.auth import login_required
from app.utils.errors import handle_errors
from app.utils.groups import get_sidebar_data


root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET'])
@login_required
@handle_errors
def index():
    user_invites, user_groups = get_sidebar_data()
    return render_template('index.html', user_groups=user_groups, user_invites=user_invites)
