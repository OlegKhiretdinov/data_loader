from flask import Flask, send_from_directory, request, render_template
import os
from urllib.parse import urljoin

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/'


@app.route('/')
def home():
    upload_folder_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        app.config['UPLOAD_FOLDER']
    )
    files = os.listdir(upload_folder_path)
    base_url = request.base_url
    files_url = map(lambda file: f'{base_url}download/{file}', files)
    return render_template('/pages/home_page.html', files=files_url)


@app.route('/download/<string:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
