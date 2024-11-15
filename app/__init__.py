from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

db = SQLAlchemy() 
def create_app():
    migrate = Migrate()
    app = Flask(__name__)

    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.secret_key = app.config['SECRET_KEY']
    migrate.init_app(app, db)
    from .routes import root_bp, groups, auth
    app.register_blueprint(root_bp)
    app.register_blueprint(groups.groups_bp)
    app.register_blueprint(auth.auth_bp)

    return app

app = create_app()