from peewee import *
from playhouse.postgres_ext import ArrayField

from back.core import db

from .base_model import BaseModel

class Region(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class RegionInfo(BaseModel):
    id = AutoField()
    region = ForeignKeyField(Region, backref='info')
    description = TextField(null=True)
    wine_style = TextField(null=True)
    history = TextField(null=True)
    weather_and_soil = TextField(null=True)
    region_map = CharField(null=True)

with db:
    Region.create_table(safe=True)
    RegionInfo.create_table(safe=True)