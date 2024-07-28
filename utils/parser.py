import csv
import re
from collections import Counter


def data_type_detector(value):
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
    new_name = re.sub(r'[^a-zA-Z_|\d]', '', name)
    if not re.search(r'\D', new_name):
        new_name = f'column_{new_name}'
    return new_name


def get_csv_columns_type(path, sep=';', has_header=None):
    columns_name = []
    columns_type_collection = []
    with (open(path) as file):
        if has_header is None:
            # Если не знаем есть ли в таблице заголовок, то пытаемся определить
            line_length = len(file.readline())
            file.seek(0)
            has_header = csv.Sniffer().has_header(file.read(line_length * 3))
            file.seek(0)

        csv_file = csv.reader(file, delimiter=sep)
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
            columns_type = list(map(lambda types: Counter(types).most_common(1)[0][0], columns_type_collection))
    return list(zip(columns_name, columns_type))
    # return list(map(lambda column: (column[0], Counter(column[1]).most_common(1)[0][0]), result))
