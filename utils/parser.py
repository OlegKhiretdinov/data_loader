import csv
import logging
import re
from collections import Counter


def data_type_detector(value):
    """
    Определяет тип данных для postgres
    :param value: any
    :return: "bigint" | "float" | "text"
    """
    try:
        int(value)
        return 'bigint'
    except ValueError:
        pass
    try:
        float(value)
        return 'float'
    except ValueError:
        pass
    return 'text'


def sanitize_column_name(name):
    """
    отсавляет в строке только буквы цифры и _
    :param name: название колонки
    :return: название колонки допустимое в Postgres
    """
    new_name = re.sub(r'[^a-zA-Z_|\d]', '', name)
    if not re.search(r'\D', new_name):
        new_name = f'column_{new_name}'
    return new_name


def get_csv_delimiter(file):
    """
    определяеи разделитель в csv файле
    :param file: файл
    :return: разделитель
    """
    line_length = len(file.readline())
    file.seek(0)
    sep = csv.Sniffer().sniff(file.read(line_length * 100)).delimiter
    file.seek(0)
    return sep


def csv_header_checker(file):
    """
    определяем есть ли заголовок
    :param file: файл
    :return: True | False
    """
    line_length = len(file.readline())
    file.seek(0)
    has_header = csv.Sniffer().has_header(file.read(line_length * 3))
    file.seek(0)
    return has_header


def csv_file_params(path, sep=None, has_header=None):
    """
    определяет параметры колонок, наличие заголовка и разделитель
    :param path: путь к csv файлу
    :param sep: разделитель
    :param has_header: флаг указывающий есть ли в таблице заголовок
    :return: объект с параметрами csv файла. типы колонок представлены списком кортежей (название колонки, тип колонки)
    """
    columns_name = []
    columns_type_collection = []

    logging.info(f'открываем файл {path}')
    with open(path) as file:
        if has_header is None:
            logging.info(f'определяем есть ли заголовок в файле {path}')
            has_header = csv_header_checker(file)

        if sep is None:
            logging.info(f'определяем разделитель в файле {path}')
            sep = get_csv_delimiter(file)

        csv_file = csv.reader(file, delimiter=sep)
        logging.info(f'определяем типы данных в файле {path}')
        for row in csv_file:
            if csv_file.line_num == 1:
                # добавляем заголовки в список параметров таблицы
                if has_header:
                    for index, value in enumerate(row):
                        name = sanitize_column_name(value)
                        if not name or name in columns_name:
                            name = f'column_{index}'
                        columns_name.append(name)
                    continue
                #  если заголовков нет, генерируем
                else:
                    for i in range(1, len(row) + 1):
                        columns_name.append(f'column_{i}')

            for index, value in enumerate(row):
                while len(columns_type_collection) <= index:
                    columns_type_collection.append([])
                # для каждой колонки записываем тип каждой записи
                columns_type_collection[index].append(data_type_detector(value))

            # Типы выводим по первым десяти строкам
            if csv_file.line_num == 10 + int(has_header):
                break

            # Отбираем наиболее встречающийся тип данных
            columns_type = list(map(
                lambda types: Counter(types).most_common(1)[0][0],
                columns_type_collection
            ))

    return {
        'columns': list(zip(columns_name, columns_type)),
        "has_header": has_header,
        "sep": sep
    }
