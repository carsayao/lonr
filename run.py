# from app import app
import markov as mk
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

def ack():
    print("\t[+] Message was received")

# Render page
@app.route("/")
def index():
    return render_template("public/index.html")

# Chat API
@socketio.on("message")
def handle_message(message):
    # 'strWho': 
    # 'strQuery':
    message.strWho
    print(f"\t[!] {message}")

@socketio.on("connect")
def test_connect():
    print("\t[+] Connected!")
    # emit('my_response', {'data': 'Connected', 'count': 0}, callback=ack)
    emit('message', {'username': 'Welcome message', 'text': "Welcome to the chatroom!"})

@socketio.on("disconnect")
def test_disconnect():
    print("\t[!] Client disconnected")

if __name__ == "__main__":
    socketio.run(app)

