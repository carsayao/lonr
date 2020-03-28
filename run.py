from markov import generate_message
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
    print(f"\t[!] User's message {message}")
    response = generate_message(message["strWho"], message["strQuery"])
    print(f"\t[!] Response {response}")
    emit("message", response)

@socketio.on("connect")
def test_connect():
    print("\t[+] Connected!")
    emit('message', {'username': 'Welcome message', 'text': "Welcome to the chatroom!"})

@socketio.on("disconnect")
def test_disconnect():
    print("\t[!] Client disconnected")

if __name__ == "__main__":
    socketio.run(app)

