from app.utils.time import time_ago

def format_message(message):
    return {
        'content': message['content'],
        'id': message['id'],
        'created_at': time_ago(message['created_at']),
        'username': message['username'],
        'user_id': message['user_id']
    }
