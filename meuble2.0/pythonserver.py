from flask import Flask, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('upload')
def handle_upload(data):
    file = data['file']
    total_size = data['totalSize']
    uploaded = 0

    with open(f'app.config["UPLOAD_FOLDER"]/{file.filename}', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
            uploaded += len(chunk)
            socketio.emit('progress', {'percentage': (uploaded / total_size) * 100})

if __name__ == '__main__':
    socketio.run(app, debug=True)
