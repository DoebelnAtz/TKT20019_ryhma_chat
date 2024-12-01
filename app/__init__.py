from flask import Flask
from flask_socketio import SocketIO
from .socket import register_socket_events, socketio
from .db import db


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile('../config.py')
    db.init_app(flask_app)
    socketio.init_app(flask_app)

    flask_app.secret_key = flask_app.config['SECRET_KEY']
    if flask_app.config['ENVIRONMENT'] == 'development':
        flask_app.debug = True

    # pylint: disable=import-outside-toplevel
    from .routes import root_bp, groups, auth, errors
    flask_app.register_blueprint(root_bp)
    flask_app.register_blueprint(errors.errors_bp)
    flask_app.register_blueprint(groups.groups_bp)
    flask_app.register_blueprint(auth.auth_bp)
    register_socket_events()
    return flask_app


app = create_app()
