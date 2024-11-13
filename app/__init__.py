from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

db = SQLAlchemy() 
def create_app():
    migrate = Migrate()
    app = Flask(__name__)

    app.config.from_pyfile('../config.py')  
    db.init_app(app)
    migrate.init_app(app, db)
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User, Group, Message, GroupInvite, UserGroup
    return app

app = create_app()