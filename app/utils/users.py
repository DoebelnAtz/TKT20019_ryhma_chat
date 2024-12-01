from werkzeug.security import generate_password_hash
from sqlalchemy import text
from app.db import db


def create_user(username, password):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING *"
    result = db.session.execute(
        text(sql), {"username": username, "password": generate_password_hash(password)})
    return result.fetchone()


def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {"username": username})
    return result.fetchone()
