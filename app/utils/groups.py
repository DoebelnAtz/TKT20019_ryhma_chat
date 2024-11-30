from flask import session, flash, redirect, url_for
from sqlalchemy import text
from app.utils.errors import HTTPError
from app.utils.users import get_user_by_username
from app import db


def get_user_group(group_id):
    sql = """
    SELECT * FROM groups 
    JOIN users_groups 
    ON groups.id = users_groups.group_id 
    WHERE groups.id = :group_id 
    AND users_groups.user_id = :user_id
    """
    result = db.session.execute(
        text(sql), {"group_id": group_id, "user_id": session['user_id']})
    return result.fetchone()


def get_user_groups():
    sql = """
    SELECT * FROM groups g 
    JOIN users_groups ug 
    ON g.id = ug.group_id 
    WHERE ug.user_id = :user_id
    """
    result = db.session.execute(text(sql), {"user_id": session['user_id']})
    return result.fetchall()


def get_user_invites():
    sql = """
    SELECT gi.id, g.name FROM group_invites gi 
    JOIN groups g ON gi.group_id = g.id
    WHERE gi.recipient_id = :user_id
    """
    result = db.session.execute(text(sql), {"user_id": session['user_id']})
    return result.fetchall()


def get_group_invite(invite_id):
    sql = "SELECT * FROM group_invites WHERE id = :invite_id"
    result = db.session.execute(text(sql), {"invite_id": invite_id})
    return result.fetchone()


def accept_group_invite(invite_id):
    invite = get_group_invite(invite_id)
    if not invite:
        flash('Invite not found.')
        return redirect(url_for('root.index'))
    if invite.recipient_id != session['user_id']:
        flash('You are not the recipient of this invite.')
        return redirect(url_for('root.index'))

    add_user_to_group(invite.group_id)
    sql = "DELETE FROM group_invites WHERE id = :invite_id"
    db.session.execute(text(sql), {"invite_id": invite_id})
    db.session.commit()


def get_group_messages(group_id):
    sql = """
    SELECT m.id, m.content, m.created_at, u.username
    FROM groups g
    JOIN users_groups ug ON g.id = ug.group_id
    JOIN users u ON ug.user_id = u.id
    JOIN messages m ON g.id = m.group_id
    WHERE g.id = :group_id
    AND ug.user_id = :user_id
    """
    result = db.session.execute(
        text(sql), {"group_id": group_id, "user_id": session['user_id']})
    return result.fetchall()


def send_group_message(group_id, content):
    group = get_user_group(group_id)
    if not group:
        flash('You are not in this group.')
        return redirect(url_for('root.index'))
    sql = """
    INSERT INTO messages (content, group_id, sender_id) 
    VALUES (:content, :group_id, :sender_id)
    """
    db.session.execute(
        text(sql),
        {
            "content": content,
            "group_id": group_id,
            "sender_id": session['user_id']
        }
    )
    db.session.commit()


def edit_user_group(group_id, name):
    sql = """
    UPDATE groups SET name = :name 
    WHERE id = :group_id 
    AND created_by = :user_id
    """
    db.session.execute(
        text(sql), {"name": name, "group_id": group_id, "user_id": session['user_id']})


def create_group(name):
    sql = "INSERT INTO groups (name, created_by) VALUES (:name, :user_id) RETURNING id"
    result = db.session.execute(
        text(sql), {"name": name, "user_id": session['user_id']})
    return result.fetchone()[0]


def add_user_to_group(group_id):
    sql = "INSERT INTO users_groups (user_id, group_id) VALUES (:user_id, :group_id)"
    db.session.execute(
        text(sql), {"user_id": session['user_id'], "group_id": group_id})


def invite_user_to_group(group_id, username):
    recipient = get_user_by_username(username)
    if not recipient:
        flash('User not found.')
        return redirect(url_for('groups.edit', group_id=group_id))

    sql = """
    INSERT INTO group_invites (group_id, sender_id, recipient_id) 
    VALUES (:group_id, :sender_id, :recipient_id)
    """
    db.session.execute(
        text(sql), {
            "group_id": group_id,
            "sender_id": session['user_id'],
            "recipient_id": recipient.id
        }
    )


def get_group_members(group_id):
    sql = """
    SELECT u.id, u.username 
    FROM users_groups ug 
    JOIN users u ON ug.user_id = u.id 
    WHERE ug.group_id = :group_id
    """
    result = db.session.execute(text(sql), {"group_id": group_id})
    return result.fetchall()


def get_group_invites(group_id):
    sql = """
    SELECT u.id, u.username FROM group_invites gi 
    JOIN users u ON gi.recipient_id = u.id 
    WHERE gi.group_id = :group_id
    """
    result = db.session.execute(text(sql), {"group_id": group_id})
    return result.fetchall()


def is_user_group_creator(group, user_id):
    return group.created_by == user_id
