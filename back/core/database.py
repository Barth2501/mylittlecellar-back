from playhouse.postgres_ext import PostgresqlExtDatabase
# from peewee import PostgresqlDatabase
from .config import config
from urllib.parse import urlparse
import os

url = urlparse(os.environ.get('DATABASE_URL'))
db = PostgresqlExtDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)