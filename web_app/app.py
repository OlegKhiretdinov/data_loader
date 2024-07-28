import os

from flask import Flask, request, render_template

from db.queries import create_table_query
from utils.loader import loader
from utils.parser import get_csv_columns_type

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_data/'


@app.route('/')
def home():
    return render_template('pages/home_page.html',)


@app.post('/download')
def download():
    url = request.form.get('url')
    temp_storage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        app.config['UPLOAD_FOLDER']
    )
    status, data = loader(url, temp_storage_path)

    if status == 200:
        columns_type = get_csv_columns_type(data)
    create_table_query(columns_type, data)
    return "Данные Загружены"
