from flask import Flask, render_template, request, redirect, url_for
import os
import secrets
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)  # Used for generating unique shareable links

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Generate a unique shareable link
def generate_shareable_link():
    return secrets.token_urlsafe(16)  # Generate a random URL-friendly token

# Initialize GoogleAuth and GoogleDrive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Handles OAuth authentication
drive = GoogleDrive(gauth)

# Routes to handle file uploads and generate shareable links
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Upload file to Google Drive
        gdrive_file = drive.CreateFile({'title': file.filename})
        gdrive_file.Upload()

        # Share the file with a specific Gmail account (replace with your Gmail)
        gdrive_file.InsertPermission({
            'type': 'user',
            'value': 'brazenowl9875@gmail.com',
            'role': 'reader'
        })

        # Generate a unique shareable link
        shareable_link = gdrive_file['alternateLink']

        return f'Shareable Link: {shareable_link}'

    return 'File upload failed'

if __name__ == '__main__':
    app.run(debug=True)
