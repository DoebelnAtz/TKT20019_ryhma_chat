from flask import session
from sqlalchemy import text
from app.utils.errors import HTTPError
from app.utils.users import get_user_by_username
from app.db import db

MAX_GROUP_NAME_LENGTH = 100
MAX_MESSAGE_LENGTH = 1000


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
    SELECT gi.id, g.name, s.username as sender_username FROM group_invites gi 
    JOIN groups g ON gi.group_id = g.id
    JOIN users s ON gi.sender_id = s.id
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
        raise HTTPError('Invite not found.', 404)
    if invite.recipient_id != session['user_id']:
        raise HTTPError('You are not the recipient of this invite.', 403)
    add_user_to_group(invite.group_id)
    sql = "DELETE FROM group_invites WHERE id = :invite_id"
    db.session.execute(text(sql), {"invite_id": invite_id})
    db.session.commit()


def decline_group_invite(invite_id):
    sql = "DELETE FROM group_invites WHERE id = :invite_id AND recipient_id = :user_id"
    db.session.execute(
        text(sql), {"invite_id": invite_id, "user_id": session['user_id']})
    db.session.commit()


def get_group_messages(group_id, limit=20):
    sql = """
    WITH user_accessible_groups AS (
        SELECT g.id FROM groups g
        JOIN users_groups ug ON g.id = ug.group_id
        WHERE ug.user_id = :user_id
    )
    SELECT m.id, m.content, m.created_at, u.username, u.id as user_id
    FROM user_accessible_groups uag
    JOIN messages m ON uag.id = m.group_id
    JOIN users u ON m.sender_id = u.id
    WHERE uag.id = :group_id
    ORDER BY m.created_at DESC
    LIMIT :limit
    """
    result = db.session.execute(
        text(sql), {"group_id": group_id, "user_id": session['user_id'], "limit": limit})
    return result.fetchall()


def send_group_message(group_id, content):
    if len(content) > MAX_MESSAGE_LENGTH:
        raise HTTPError('Message too long.', 400)
    group = get_user_group(group_id)
    if not group:
        raise HTTPError('Group not found.', 404)
    sql = """
    INSERT INTO messages (content, group_id, sender_id) 
    VALUES (:content, :group_id, :sender_id)
    RETURNING id, content, created_at
    """
    result = db.session.execute(
        text(sql),
        {
            "content": content,
            "group_id": group_id,
            "sender_id": session['user_id']
        }
    )
    db.session.commit()
    created_message = result.fetchone()
    message = {
        "id": created_message.id,
        "content": created_message.content,
        "created_at": created_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "username": session['username'],
        "user_id": session['user_id']
    }
    return message


def is_group_creator(group_id):
    return is_user_group_creator(get_user_group(group_id), session['user_id'])


def edit_user_group(group_id, name):
    if len(name) > MAX_GROUP_NAME_LENGTH:
        raise HTTPError('Name too long.', 400)
    sql = """
    UPDATE groups SET name = :name 
    WHERE id = :group_id 
    AND created_by = :user_id
    """
    db.session.execute(
        text(sql), {"name": name, "group_id": group_id, "user_id": session['user_id']})


def create_group(name):
    if len(name) > MAX_GROUP_NAME_LENGTH:
        raise HTTPError('Name too long.', 400)
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
        raise HTTPError('User not found.', 404)

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


def leave_user_group(group_id):
    sql = "DELETE FROM users_groups WHERE user_id = :user_id AND group_id = :group_id"
    db.session.execute(
        text(sql), {"user_id": session['user_id'], "group_id": group_id})


def delete_user_group(group_id):
    if not is_group_creator(group_id):
        raise HTTPError('You are not the creator of this group.', 403)

    sql = "DELETE FROM groups WHERE id = :group_id AND created_by = :user_id"
    db.session.execute(
        text(sql), {"group_id": group_id, "user_id": session['user_id']})


def get_sidebar_data():
    return get_user_invites(), get_user_groups()
