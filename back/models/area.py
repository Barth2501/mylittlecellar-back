from peewee import *
from playhouse.postgres_ext import ArrayField

from .base_model import BaseModel
from .region import Region
from .cellar import Cellar
from back.core import db
from playhouse.migrate import *


migrator = PostgresqlMigrator(db)

class Area(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    region = ForeignKeyField(Region, backref='areas', null=True)

    def modify_region(self, region):
        return Area.update(region=region).where(Area.name==self.name).execute()

    def get_info(self):
        return AreaInfo.get_or_none(area=self).get_small_data()

    def get_data_region(self):
        data= self.get_small_data()
        region = Region.get_by_id(self.region).get_small_data()
        for key in region.keys():
            data['region_'+key] = region[key]
        return data

    def get_info_data(self):
        data = self.get_small_data()
        data['info'] = self.get_info()
        return data

    def get_grapes(self):
        return [g.grape.get_small_data() for g in self.grapes]

    def get_info_grapes_data(self):
        data = self.get_small_data()
        data['info'] = self.get_info()
        data['grapes'] = self.get_grapes()
        return data

    def get_data_number(self, cellar_id):
        data = self.get_small_data()
        cellar_area = CellarArea.get_or_none(area=self, cellar=cellar_id)
        if cellar_area:
            data['wines_nb']= cellar_area.number
        return data

class AreaInfo(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='info')
    description = TextField(null=True)
    photo = CharField(null=True)
    keep_advise = TextField(null=True)
    eye = TextField(null=True)
    nose = TextField(null=True)
    mouth = TextField(null=True)
    food = TextField(null=True)

class Grape(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    color = CharField(null=True)
    description = TextField(null=True)

class GrapeSynonym(BaseModel):
    id = AutoField()
    grape_1 = ForeignKeyField(Grape, backref='synonym')
    grape_2 = ForeignKeyField(Grape, backref='synonym')

class AreaGrape(BaseModel):
    id = AutoField()
    grape = ForeignKeyField(Grape, backref='areas')
    area = ForeignKeyField(Area, backref='grapes')

class CellarArea(BaseModel):
    id = AutoField()
    cellar = ForeignKeyField(Cellar, backref='areas')
    area = ForeignKeyField(Area, backref='cellars')
    number = IntegerField(null=True)

    def modify_number(self, number):
        return CellarArea.update(number=self.number+number).where(CellarArea.cellar==self.cellar,CellarArea.area==self.area).execute()

class AreaVintage(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='vintage')
    color = CharField()
    vintage = TextField()

    def add_rank(self, year, rank):
        #vintage_list = self.vintage
        #vintage_list = vintage_list +",{'vintage':{},'rank':{}}".format(year,rank)
        data = {'vintage': year, 'rank': rank}
        AreaVintage.update({
                AreaVintage.vintage: AreaVintage.vintage.concat(data)
            }).where(AreaVintage.id==self).execute()
        return AreaVintage.update({
                AreaVintage.vintage: AreaVintage.vintage.concat(',')
            }).where(AreaVintage.id==self).execute()

class AreaDetail(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='detail')
    color = CharField(null=True)
    age_min = IntegerField(null=True)
    age_max = IntegerField(null=True)
    t_min = IntegerField(null=True)
    t_max = IntegerField(null=True)
    glass_type = CharField(null=True)
    comments = TextField(null=True)


with db:
    Area.create_table(safe=True)
    AreaInfo.create_table(safe=True)
    Grape.create_table(safe=True)
    AreaGrape.create_table(safe=True)
    GrapeSynonym.create_table(safe=True)
    CellarArea.create_table(safe=True)
    AreaVintage.create_table(safe=True)
    AreaDetail.create_table(safe=True)