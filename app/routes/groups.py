from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from sqlalchemy import text
from app import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        createdGroup = create_group(name)
        add_user_to_group(createdGroup)
        db.session.commit()
        return redirect(url_for('root.index'))
    else:
        return render_template('groups/create.html')


@groups_bp.route("/<int:group_id>", methods=('GET','POST'))
def group(group_id):
    group = get_user_group(group_id)
    if request.method == 'POST':
        content = request.form['content']
        send_group_message(group_id, content)
        return redirect(url_for('groups.group', group_id=group_id))
    else:
        messages = get_user_messages(group_id)
        return render_template('groups/group.html', group=group, messages=messages)


@groups_bp.route("/edit/<int:group_id>", methods=('GET', 'POST'))
def edit(group_id):
    if request.method == 'POST':
        name = request.form['name']
        edit_user_group(group_id, name)
        db.session.commit()
        return redirect(url_for('groups.group', group_id=group_id))
    else:
        group = get_user_group(group_id)
        return render_template('groups/edit.html', group=group)


def get_user_group(group_id,):
    sql = """
    SELECT * FROM groups 
    JOIN users_groups 
    ON groups.id = users_groups.group_id 
    WHERE groups.id = :group_id 
    AND users_groups.user_id = :user_id
    """
    result = db.session.execute(text(sql), {"group_id": group_id, "user_id": session['user_id']})
    return result.fetchone()


def get_user_messages(group_id):
    sql = """
    SELECT m.id, m.content, m.created_at, u.username
    FROM groups g
    JOIN users_groups ug ON g.id = ug.group_id
    JOIN users u ON ug.user_id = u.id
    JOIN messages m ON g.id = m.group_id
    WHERE g.id = :group_id
    AND ug.user_id = :user_id
    """
    result = db.session.execute(text(sql), {"group_id": group_id, "user_id": session['user_id']})
    return result.fetchall()

def send_group_message(group_id, content):
    group = get_user_group(group_id)
    if not group:
        flash('You are not in this group.')
        return redirect(url_for('root.index'))
    sql = "INSERT INTO messages (content, group_id, sender_id) VALUES (:content, :group_id, :sender_id)"
    db.session.execute(text(sql), {"content": content, "group_id": group_id, "sender_id": session['user_id']})
    db.session.commit()

def edit_user_group(group_id, name):
    sql = "UPDATE groups SET name = :name WHERE id = :group_id AND created_by = :user_id"
    db.session.execute(text(sql), {"name": name, "group_id": group_id, "user_id": session['user_id']})

def create_group(name):
    sql = "INSERT INTO groups (name, created_by) VALUES (:name, :user_id) RETURNING id"
    result = db.session.execute(text(sql), {"name": name, "user_id": session['user_id']})
    return result.fetchone()[0]

def add_user_to_group(group_id):
    sql = "INSERT INTO users_groups (user_id, group_id) VALUES (:user_id, :group_id)"
    db.session.execute(text(sql), {"user_id": session['user_id'], "group_id": group_id})
