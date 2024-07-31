import logging
import os
import re

import requests

AVAILABLE_EXT = {"text/csv": "csv"}


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
    # определение расширения файла
    content_type = re.search(
        r'[a-z]*\/[a-z]*',
        response.headers.get('Content-Type', '')
    )
    f_type = content_type.group(0) if content_type else ''

    if f_type not in AVAILABLE_EXT:
        logging.warning(f'не допустимое расширение файла {url}')
        return 0, "не допустимое расширение файла"

    # определение имени файла
    desc_file_name = re.search(
        r'(?<=filename=).*\.\S*',
        response.headers.get('Content-Disposition', '')
    )
    f_name = desc_file_name.group(0) if desc_file_name else f'file.{AVAILABLE_EXT[f_type]}'

    filepath = os.path.join(local_path, f_name)
    suffix = 0

    while os.path.exists(filepath):
        suffix += 1
        name, _ = os.path.splitext(f_name)
        filepath = os.path.join(local_path, f"{name}-{suffix}.{AVAILABLE_EXT[f_type]}")

    try:
        logging.warning(f'сохраняем файл {filepath}')
        with open(filepath, "w") as f:
            f.write(response.content.decode())
    except OSError as exc:
        logging.error(f'не удалось сохранить файл {filepath}: {exc.strerror}')
        return 0, "не удалось сохранить файл"

    logging.warning(f'файл {filepath} сохранён')
    return response.status_code, filepath
