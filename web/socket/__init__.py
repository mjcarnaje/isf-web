from flask import current_app
from flask_socketio import SocketIO, emit
from flask_login import current_user
from ..utils import authenticated_only

socketio = SocketIO()

connected_users = set()

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        user_id = str(current_user.id)
        connected_users.add(user_id)
        current_app.logger.info(f"User {user_id} connected")

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        user_id = str(current_user.id)
        connected_users.discard(user_id)
        current_app.logger.info(f"User {user_id} disconnected")

def handle_notification(user_id, data):
    current_app.logger.info('Handle notification')
    user_id_str = str(user_id)
    if user_id_str in connected_users:
        socketio.emit('notification', data)
    else:
        current_app.logger.info(f"User {user_id_str} is not connected")
