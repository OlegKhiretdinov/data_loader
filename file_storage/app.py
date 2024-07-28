from flask import Flask, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/'


@app.route('/download/<string:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
