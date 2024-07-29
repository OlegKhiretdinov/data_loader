import os

from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()
# DATABASE_URL = os.getenv('DATABASE_URL')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

print("POSTGRES_ENV", POSTGRES_HOST)

DATABASE_URL = f"user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB}"

connections = pool.SimpleConnectionPool(1, 100, DATABASE_URL)
