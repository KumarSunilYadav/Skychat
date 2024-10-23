from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'  # You should use a secure key for session management.
socketio = SocketIO(app)

# Store the connection time for each user and their names
connected_users = {}

@app.route('/')
def index():
    return render_template('index.html')

# Handle a user connecting to the server
@socketio.on('connect')
def handle_connect():
    # Prompt for username when a user connects
    emit('request_username')

# Handle username assignment when a user connects
@socketio.on('set_username')
def handle_set_username(data):
    username = data.get('username', 'Anonymous')
    connected_users[request.sid] = username
    # Notify everyone that a user has connected
    emit('user_connected', {'username': username, 'sid': request.sid}, broadcast=True)

# Handle incoming messages from users
@socketio.on('message')
def handle_message(msg):
    username = connected_users.get(request.sid, 'Anonymous')
    # Broadcast the message to all connected clients
    emit('message', {'msg': msg, 'username': username}, broadcast=True)

# Handle a user disconnecting from the server
@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.pop(request.sid, 'Anonymous')
    # Notify everyone that a user has disconnected
    emit('user_disconnected', {'username': username, 'sid': request.sid}, broadcast=True)

# Run the application
if __name__ == '__main__':
    # Use the $PORT environment variable if it's set, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
