from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy() 
def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.secret_key = app.config['SECRET_KEY']
    if app.config['ENVIRONMENT'] == 'development':
        app.debug = True

    from .routes import root_bp, groups, auth
    app.register_blueprint(root_bp)
    app.register_blueprint(groups.groups_bp)
    app.register_blueprint(auth.auth_bp)

    return app

app = create_app()