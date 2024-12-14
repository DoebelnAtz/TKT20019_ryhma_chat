from flask_socketio import join_room, send, SocketIO
from flask import session
from app.utils.groups import send_group_message
from app.utils.errors import handle_socket_errors
from app.utils.logger import Logger

logger = Logger('Socket')
socketio = SocketIO(cors_allowed_origins=['http://127.0.0.1:5000', 'http://localhost:5000', 'https://taival.app'])


def register_socket_events():
    @socketio.on('connected')
    @handle_socket_errors
    def handle_connected(data):
        logger.debug('connected', data)
        join_room(session['user_id'])

    @socketio.on('join_group')
    @handle_socket_errors
    def handle_join_group(data):
        logger.debug('join_group', data)
        join_room(data['group_id'])

    @socketio.on('message')
    @handle_socket_errors
    def handle_message(data):
        logger.debug('message', data)
        created_message = send_group_message(data['group_id'], data['content'])
        send(created_message, room=data['group_id'], namespace='/')

    logger.debug('Socket events registered')
