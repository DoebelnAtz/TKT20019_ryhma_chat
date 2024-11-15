from flask import Blueprint, render_template, session
from sqlalchemy import text
from app import db

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    result = db.session.execute(text("""
        SELECT * FROM groups JOIN users_groups ON groups.id = users_groups.group_id
        WHERE users_groups.user_id = :user_id
    """), {"user_id": session['user_id']})
    groups = result.fetchall()
    print(groups)
    return render_template('index.html', groups=groups)
