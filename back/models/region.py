from peewee import *
from playhouse.postgres_ext import ArrayField

from back.core import db

from .base_model import BaseModel
from .cellar import Cellar

class Region(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

    def get_data_map(self):
        data = self.get_small_data()
        data['map'] = self.info.get().get_small_data()['region_map']
        return data

    def get_info_data(self):
        data = self.get_small_data()
        data['info'] = self.info.get().get_small_data()
        return data

class RegionInfo(BaseModel):
    id = AutoField()
    region = ForeignKeyField(Region, backref='info')
    description = TextField(null=True)
    wine_style = TextField(null=True)
    history = TextField(null=True)
    weather_and_soil = TextField(null=True)
    region_map = CharField(null=True)
    photo = CharField(null=True)

class CellarRegion(BaseModel):
    id = AutoField()
    cellar = ForeignKeyField(Cellar, backref='region')
    region = ForeignKeyField(Region, backref='cellar')
    number = IntegerField(null=True)
    
    def modify_number(self, number):
        return CellarRegion.update(number=self.number+number).where(CellarRegion.cellar==self.cellar,CellarRegion.region==self.region).execute()

    def get_region_number(self):
        data = self.get_small_data()
        data['region_name'] = self.region.get_small_data()['name']
        return data

    def update_number(self, number):
        if self.number+number==0:
            return self.delete_instance()
        else:
            return CellarRegion.update(number=self.number+number).where(CellarRegion.cellar==self.cellar,CellarRegion.region==self.region).execute()

with db:
    Region.create_table(safe=True)
    RegionInfo.create_table(safe=True)
    CellarRegion.create_table(safe=True)