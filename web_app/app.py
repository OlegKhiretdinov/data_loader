import logging
import os
from urllib.parse import urlparse

from flask import Flask, request, render_template

from db.queries import create_table_query
from utils.loader import loader
from utils.parser import get_csv_columns_type

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_data/'
temp_storage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        app.config['UPLOAD_FOLDER']
    )


@app.route('/')
def home():
    return render_template('pages/home_page.html')


@app.post('/download')
def download():
    url = request.form.get('url')
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.path]):
        logging.info(f'не валидный url {url}')
        return render_template('pages/home_page.html')

    status, data = loader(url, temp_storage_path)

    if status == 200:
        columns_type = get_csv_columns_type(data)
        create_table_query(columns_type, data)
        return "Данные Загружены"
    else:
        return f'Не удалось загрузить данные. {data}'
