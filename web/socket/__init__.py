from flask_socketio import SocketIO, emit
from flask_login import current_user
from ..utils import authenticated_only

socketio = SocketIO()

connected_users = set()

@socketio.on('connect')
@authenticated_only
def handle_connect():
    user_id = current_user.id
    connected_users.add(str(user_id))
    print(f"User {user_id} connected")

@socketio.on('disconnect')
@authenticated_only
def handle_disconnect():
    user_id = current_user.id
    connected_users.discard(str(user_id))
    print(f"User {user_id} disconnected")

def handle_notification(user_id, data):
    print('Handle notification')
    print(user_id)
    print(type(user_id))
    if str(user_id) in connected_users:
        socketio.emit('notification', data)
    else:
        print(f"User {user_id} is not connected")
