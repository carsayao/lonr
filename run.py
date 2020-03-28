# from app import app
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Render page
@app.route("/")
def index():
    return render_template("public/index.html")

# Chat API
@socketio.on("connect")
def test_connect():
    print("[+] Connected!")
    emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == "__main__":
    socketio.run(app)

