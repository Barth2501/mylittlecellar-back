from playhouse.postgres_ext import PostgresqlExtDatabase
# from peewee import PostgresqlDatabase
from .config import config
from urllib.parse import urlparse

url = urlparse('postgres://mjxjszztlfhttf:cfe81c3a20b8a422838a2e944eaa7d64012df025ce3ae04d1e565ccfd87d5763@ec2-176-34-97-213.eu-west-1.compute.amazonaws.com:5432/d8k6to5ro8o4e7')
db = PostgresqlExtDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)