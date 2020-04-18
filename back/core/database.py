# from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import PostgresqlDatabase
from .config import config
from urllib.parse import urlparse

url = urlparse('postgres://sajlrqdaakhmxf:c459334dcbab2bdfcf56b6b5e49b581bd4483e7aeca6604480280b19e95ed57d@ec2-18-210-51-239.compute-1.amazonaws.com:5432/d3757og6vdih1')
db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)