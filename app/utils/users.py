from werkzeug.security import generate_password_hash
from app import db
from sqlalchemy import text

def create_user(username, password):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING *"
    result = db.session.execute(text(sql), {"username": username, "password": generate_password_hash(password)})
    return result.fetchone()

def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {"username": username})
    return result.fetchone()
