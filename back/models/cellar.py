from peewee import *

from back.core import db

from .base_model import BaseModel
from .user import User

class Cellar(BaseModel):
    id = AutoField()
    name = CharField()
    user = ForeignKeyField(User, backref='cellars')

with db:
    Cellar.create_table(safe=True)
