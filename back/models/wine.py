from peewee import *
from .base_model import BaseModel
from .winery import Winery
from .area import Area
from .cellar import Cellar
from .region import Region
from back.core import db


class Wine(BaseModel):
    id = AutoField()
    winery = ForeignKeyField(Winery, backref='wines')
    name = TextField()
    vintage = IntegerField()
    mark = FloatField(null=True)
    advise = TextField(null=True)

    def get_data(self):
        data = self.get_small_data()
        data['winery'] = self.winery.get_small_data()
        data['area'] = self.winery.area.get_small_data()
        return data

    def get_all_data_number(self, cellar_id):
        data = self.get_small_data()
        winery = Winery.get_by_id(self.winery).get_small_data()
        for key in winery.keys():
            data['winery_'+key] = winery[key]
        area = Area.get_by_id(winery['area']).get_small_data()
        for key in area.keys():
            data['area_'+key] = area[key]
        region = Region.get_by_id(area['region']).get_small_data()
        for key in region.keys():
            data['region_'+key] = region[key]
        data['number'] = CellarWine.get(cellar=cellar_id,wine=self).get_small_data()['number']
        return data

    def get_data_number(self, cellar_id):
        data = self.get_small_data()
        data['number'] = CellarWine.get(cellar=cellar_id,wine=self).get_small_data()['number']
        return data

class CellarWine(BaseModel):
    id = AutoField()
    cellar = ForeignKeyField(Cellar, backref='wines')
    wine = ForeignKeyField(Wine, backref='cellars')
    number = IntegerField()

    def modify_number(self, number):
        return CellarWine.update(number=self.number+number).where(CellarWine.cellar==self.cellar,CellarWine.wine==self.wine).execute()

with db:
    Wine.create_table(safe=True)
    CellarWine.create_table(safe=True)