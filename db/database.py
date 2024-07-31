import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool, OperationalError
import logging


load_dotenv()

connection_params = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}


class ConnectionPool:
    __temp_conn = set()

    def __init__(self):
        try:
            logging.warning('Подключение к базе данных')
            self.__conn_pool = pool.SimpleConnectionPool(
                1,
                1,
                **connection_params
            )
        except OperationalError:
            logging.error('Не удалось подключиться к базе данных')
            self.__conn_pool = None

    @property
    def is_connected(self):
        return bool(self.__conn_pool)

    def getconn(self):
        try:
            return self.__conn_pool.getconn()
        except pool.PoolError as ex:
            logging.error(ex)
            connection = psycopg2.connect(**connection_params)
            self.__temp_conn.add(connection)
            return connection

    def putconn(self, connection):
        if connection in self.__temp_conn:
            self.__temp_conn.discard(connection)
        else:
            self.__conn_pool.putconn(connection)


connections = ConnectionPool()
