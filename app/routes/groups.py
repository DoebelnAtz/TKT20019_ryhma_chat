from flask import Blueprint, request, render_template, redirect, url_for, session
from app.utils.groups import decline_group_invite, get_user_group, get_group_messages
from app.utils.groups import create_group, add_user_to_group
from app.utils.groups import edit_user_group, invite_user_to_group, get_group_members
from app.utils.groups import get_group_invites, is_user_group_creator
from app.utils.groups import accept_group_invite, leave_user_group, delete_user_group
from app.utils.groups import get_sidebar_data
from app.utils.auth import login_required, csrf_required
from app.utils.messages import format_message
from app.db import db
from app.utils.errors import HTTPError, handle_errors
groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/create', methods=('GET', 'POST'))
@login_required
@handle_errors
@csrf_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        created_group_id = create_group(name)
        add_user_to_group(created_group_id)
        db.session.commit()
        return redirect(url_for('groups.edit', group_id=created_group_id))
    else:
        user_invites, user_groups = get_sidebar_data()
        return render_template('groups/create.html',
                               user_invites=user_invites,
                               user_groups=user_groups)


@groups_bp.route("/<int:group_id>", methods=['GET'])
@login_required
@handle_errors
def group(group_id):
    pages = int(request.args.get('pages', 1))
    user_group = get_user_group(group_id)
    if not user_group:
        raise HTTPError('Group not found.', 404)
    members = get_group_members(group_id)

    limit = pages * 30
    messages = get_group_messages(group_id, limit=limit)
    has_more_messages = len(messages) == limit
    user_invites, user_groups = get_sidebar_data()
    messages_serializable = [
        format_message({
            "id": message[0],
            "content": message[1],
            "created_at": message[2],
            "username": message[3],
            "user_id": message[4]
        })
        for message in messages]

    return render_template('groups/group.html',
                           group=user_group,
                           messages=messages_serializable,
                           is_user_group_creator=is_user_group_creator(
                               user_group, session['user_id']),
                           pages=pages,
                           has_more_messages=has_more_messages,
                           members=members,
                           user_groups=user_groups,
                           user_invites=user_invites)


@groups_bp.route("/edit/<int:group_id>", methods=('GET', 'POST'))
@login_required
@handle_errors
@csrf_required
def edit(group_id):
    if request.method == 'POST':
        name = request.form['name']
        edit_user_group(group_id, name)
        db.session.commit()
        return redirect(url_for('groups.group', group_id=group_id))
    else:
        user_group = get_user_group(group_id)
        group_invites = get_group_invites(group_id)
        members = get_group_members(group_id)
        user_invites, user_groups = get_sidebar_data()
        is_creator = is_user_group_creator(user_group, session['user_id'])
        return render_template('groups/edit.html',
                               group=user_group,
                               members=members,
                               group_invites=group_invites,
                               is_creator=is_creator,
                               user_groups=user_groups,
                               user_invites=user_invites)


@groups_bp.route("/edit/<int:group_id>/invite", methods=['POST'])
@login_required
@handle_errors
@csrf_required
def invite(group_id):
    username = request.form['username']
    invite_user_to_group(group_id, username)
    db.session.commit()
    return redirect(url_for('groups.edit', group_id=group_id))


@groups_bp.route("/<int:invite_id>/accept_invite", methods=['POST'])
@login_required
@handle_errors
@csrf_required
def accept_invite(invite_id):
    value = request.form['decision']
    if value == 'true':
        accept_group_invite(invite_id)
    elif value == 'false':
        decline_group_invite(invite_id)
    db.session.commit()
    return redirect(url_for('root.index'))


@groups_bp.route("/<int:group_id>/leave", methods=['POST'])
@login_required
@handle_errors
@csrf_required
def leave(group_id):
    leave_user_group(group_id)
    db.session.commit()
    return redirect(url_for('root.index'))


@groups_bp.route("/<int:group_id>/delete", methods=['POST'])
@login_required
@handle_errors
@csrf_required
def delete(group_id):
    delete_user_group(group_id)
    db.session.commit()
    return redirect(url_for('root.index'))
