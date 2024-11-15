from app.app import app, db
from app.models import User, Group, Message, GroupInvite, UserGroup


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Group': Group, 'Message': Message, 'GroupInvite': GroupInvite, 'UserGroup': UserGroup}


if __name__ == '__main__':
    app.run(debug=True)