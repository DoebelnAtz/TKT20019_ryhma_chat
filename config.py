import os

SQLALCHEMY_DATABASE_URI = "postgresql://marvin:42@localhost:6543/deep_thought"
SESSION_TYPE = "filesystem"
SECRET_KEY = os.getenv('SECRET_KEY')
TEMPLATES_AUTO_RELOAD = True
ENVIRONMENT = os.getenv('FLASK_ENV')