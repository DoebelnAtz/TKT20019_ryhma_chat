from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.utils.groups import get_user_group, get_group_messages, create_group, add_user_to_group, edit_user_group, invite_user_to_group, get_group_members, is_user_group_creator, send_group_message, get_group_invites
from app.utils.auth import login_required
from app.utils.groups import accept_group_invite
from app import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/create', methods=('GET','POST'))
@login_required
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
@login_required
def group(group_id):
    group = get_user_group(group_id)
    if request.method == 'POST':
        content = request.form['content']
        send_group_message(group_id, content)
        return redirect(url_for('groups.group', group_id=group_id))
    else:
        messages = get_group_messages(group_id)
        return render_template('groups/group.html', group=group, messages=messages, is_user_group_creator=is_user_group_creator(group, session['user_id']))


@groups_bp.route("/edit/<int:group_id>", methods=('GET', 'POST'))
@login_required
def edit(group_id):
    if request.method == 'POST':
        name = request.form['name']
        edit_user_group(group_id, name)
        db.session.commit()
        return redirect(url_for('groups.group', group_id=group_id))
    else:
        group = get_user_group(group_id)
        invites = get_group_invites(group_id)
        members = get_group_members(group_id)  
        return render_template('groups/edit.html', group=group, members=members, invites=invites)

@groups_bp.route("/edit/<int:group_id>/invite", methods=['POST'])
@login_required
def invite(group_id):
    username = request.form['username']
    invite_user_to_group(group_id, username)
    db.session.commit()
    return redirect(url_for('groups.edit', group_id=group_id))

@groups_bp.route("/<int:invite_id>/accept_invite", methods=['POST'])
@login_required
def accept_invite(invite_id):
    accept_group_invite(invite_id)
    db.session.commit()
    return redirect(url_for('root.index'))