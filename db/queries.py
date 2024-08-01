import datetime
import logging

import psycopg2
import psycopg2.errors

from db.database import connections


def create_table_query_builder(table_column_data, table_name):
    return f'''CREATE TABLE {table_name} (
            id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            {','.join(f"{name} {column_type}" for name, column_type in table_column_data)}
        );'''


def insert_data_query_builder(table_column_data, table_name):
    return f'''INSERT INTO {table_name} (
        {','.join(f"{name}" for name, _ in table_column_data)})
        VALUES ({', '.join("%s" for _ in table_column_data)})
    '''


def table_name_generator():
    return f'table_{int(datetime.datetime.utcnow().timestamp())}'


def upload_from_csv_query(csv_file_data, file_path, table_name=None):
    if not table_name:
        table_name = table_name_generator()

    create_table_query_str = create_table_query_builder(csv_file_data["columns"], table_name)
    insert_data_query_str = insert_data_query_builder(csv_file_data["columns"], table_name)

    if not connections.is_connected:
        return False, 'Не удалось подключитьяс к базе данных'

    with connections.getconn() as conn:
        with conn.cursor() as cursor:
            logging.warning(f'создание таблицы {table_name}')
            try:
                cursor.execute(create_table_query_str)
            except psycopg2.Error:
                logging.error(f'ошибка при создании таблицы {table_name}')
                return False, f'не удалось создать таблицу {table_name}'

            try:
                with open(file_path) as file:
                    if csv_file_data["has_header"]:
                        next(file)

                    logging.warning(f'добавление данных в таблицу {table_name}')
                    try:
                        for row in file:
                            cursor.execute(
                                insert_data_query_str,
                                row.strip().split(csv_file_data["sep"])
                            )
                    except IndexError:
                        logging.error(f'ошибка в файле {file_path}')
                        return False, 'ошибка в файле'
            except psycopg2.Error:
                logging.error(f'не удалось добавить данные в таблицу {table_name}')
                return False, f'не удалось добавить данные в таблицу {table_name}'
            except OSError:
                logging.error(f'ошибка при открытии файла {file_path}')
                return False, f'не удалось добавить данные в таблицу {table_name}'

    logging.warning(f'таблица {table_name} создана')
    connections.putconn(conn)
    return True, f'Данные загружены в таблицу {table_name}'
