from peewee import *
from .base_model import BaseModel
from .area import Area

from back.core import db

class Winery(BaseModel):
    id = AutoField()
    name = TextField()
    description = TextField()
    area = ForeignKeyField(Area, backref='wineries')

with db:
    Winery.create_table(safe=True)