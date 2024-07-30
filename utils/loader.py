import os
from urllib.parse import urlparse
import logging

import requests

AVAILABLE_EXT = [".csv"]


def loader(url, local_path):
    """
    скачивает файл и сохраняет локально
    :param url: url для скачивания
    :param local_path: путь к директории где будет сохранён файл
    :return: код ответа и путь  до файла в локальном хранилище или сообщение об ошибке
    """

    response = requests.get(url)
    if not response.ok:
        logging.warning(f'не удалось скачать файл {url}')
        return response.status_code, response.reason

    filename = os.path.basename(urlparse(url).path)
    f_name, f_ext = os.path.splitext(filename)

    if f_ext not in AVAILABLE_EXT:
        logging.warning(f'не допустимое расширение файла {url}')
        return 0, "не допустимое расширение файла"

    filepath = os.path.join(local_path, filename)
    suffix = 0

    while os.path.exists(filepath):
        suffix += 1
        filepath = os.path.join(local_path, f"{f_name}-{suffix}{f_ext}")

    try:
        logging.warning(f'сохраняем файл {filepath}')
        with open(filepath, "w") as f:
            f.write(response.content.decode())
    except OSError as exc:
        logging.error(f'не удалось сохранить файл {filepath}: {exc.strerror}')
        return 0, "не удалось сохранить файл"
    logging.warning(f'файл {filepath} сохранён')

    return response.status_code, filepath
