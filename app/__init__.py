from flask import Flask
from flask_socketio import SocketIO
from .socket import register_socket_events, socketio
from .db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    socketio.init_app(app)

    app.secret_key = app.config['SECRET_KEY']
    if app.config['ENVIRONMENT'] == 'development':
        app.debug = True

    from .routes import root_bp, groups, auth, errors
    app.register_blueprint(root_bp)
    app.register_blueprint(errors.errors_bp)
    app.register_blueprint(groups.groups_bp)
    app.register_blueprint(auth.auth_bp)
    register_socket_events()
    return app


app = create_app()
