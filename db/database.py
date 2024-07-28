import os

from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

connections = pool.SimpleConnectionPool(1, 100, DATABASE_URL)
