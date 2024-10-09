from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Store the connection time for each user and their names
connected_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Prompt for username when a user connects
    emit('request_username')

@socketio.on('set_username')
def handle_set_username(data):
    connected_users[request.sid] = data['username']
    emit('user_connected', {'username': data['username'], 'sid': request.sid}, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = connected_users.get(request.sid, "Anonymous")
    emit('message', {'msg': msg, 'username': username}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.get(request.sid, "Anonymous")
    if request.sid in connected_users:
        del connected_users[request.sid]
    emit('user_disconnected', {'username': username, 'sid': request.sid}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
