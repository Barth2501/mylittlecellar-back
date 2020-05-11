from peewee import *
from .base_model import BaseModel
from .area import Area
from .cellar import Cellar

from back.core import db

class Winery(BaseModel):
    id = AutoField()
    name = TextField()
    description = TextField()
    area = ForeignKeyField(Area, backref='wineries')

    def get_data_number(self, cellar_id):
        data = self.get_small_data()
        wines_nb = 0
        for wine in self.wines:
            wines_nb += wine.get_data_number(cellar_id)['number']
        data['wines_nb'] = wines_nb
        return data

    def get_names_number(self, cellar_id):
        data = {}
        data['id']=self.id
        data['name']=self.name
        data['area_name']=self.area.name
        data['region_name']=self.area.region.name
        data['number'] = CellarWinery.get_or_none(winery=self, cellar=cellar_id).number
        return data

class CellarWinery(BaseModel):
    id = AutoField()
    cellar = ForeignKeyField(Cellar, backref='wineries')
    winery = ForeignKeyField(Winery, backref='cellars')
    number = IntegerField(null=True)
    
    def modify_number(self, number):
        return CellarWinery.update(number=self.number+number).where(CellarWinery.cellar==self.cellar,CellarWinery.winery==self.winery).execute()

    def update_number(self, number):
        if self.number+number==0:
            return self.delete_instance()
        else:
            return CellarWinery.update(number=self.number+number).where(CellarWinery.cellar==self.cellar,CellarWinery.winery==self.winery).execute()


with db:
    Winery.create_table(safe=True)
    CellarWinery.create_table(safe=True)