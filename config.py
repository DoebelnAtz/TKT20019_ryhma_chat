import os

DB_NAME = os.getenv('DB_NAME', 'deep_thought')
DB_USER = os.getenv('DB_USER', 'marvin')
DB_PORT = os.getenv('DB_PORT', 6543)
DB_PASSWORD = os.getenv('DB_PASSWORD', '42')
DB_HOST = os.getenv('DB_HOST', 'localhost')
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SESSION_TYPE = "filesystem"
SECRET_KEY = os.getenv('SECRET_KEY')
TEMPLATES_AUTO_RELOAD = True
ENVIRONMENT = os.getenv('FLASK_ENV')
