from peewee import *
import json
from .base_model import BaseModel
from .winery import Winery
from .area import Area, AreaDetail, AreaVintage
from .cellar import Cellar
from .region import Region
from back.core import db
from back.controllers.aging_model import aging_model as aging_model

from playhouse.migrate import *


migrator = PostgresqlMigrator(db)

class Wine(BaseModel):
    id = AutoField()
    winery = ForeignKeyField(Winery, backref='wines')
    name = TextField()
    vintage = IntegerField()
    mark = FloatField(null=True)
    advise = CharField(null=True)
    color = CharField(null=True)

    def get_trend(self):
        data = {}
        # Rentrer le modèle de vieillissement ici
        winery = Winery.get_by_id(self.winery)
        area = Area.get_by_id(winery.area)
        
        # si on a les details des appellations en question
        area_detail = AreaDetail.get_or_none(area=area, color=self.color)
        if not area_detail:
            area_detail = AreaDetail.get_or_none(area=area)
            if not area_detail:
                print('No Detail for this area')
                age_min = 2
                age_max = 30
            else:
                age_min, age_max = int(area_detail.age_min), int(area_detail.age_max)
        else:
            age_min, age_max = int(area_detail.age_min), int(area_detail.age_max)

        # on s'intéresse aux millésimes s'il peut etre trouver dans la bdd
        if self.vintage==0 or self.vintage>2013:
            # on met le rang moyen
            print('vintage above 2013')
            rank = 5
        else:
            area_vintage = AreaVintage.get_or_none(area=area, color=self.color)
            if not area_vintage:
                area_vintage = AreaVintage.get_or_none(area=area, color='no color')
            if not area_vintage:
                print('No vintage for this area')
                rank = 5
            else:
                vintage_dict = str(area_vintage.vintage).replace("'",'"').replace('},{',',').replace(' ','')
                vintage_dict = json.loads(vintage_dict[:-1])
                if str(self.vintage) not in vintage_dict.keys():
                    print('Vintage not found')
                    rank = 5
                else:
                    rank = vintage_dict[str(self.vintage)]
        data['value'],data['year'] = aging_model.aging_model(self.vintage, age_max, age_min, rank)
        return data

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
        cellar_wine = CellarWine.get(cellar=cellar_id,wine=self)
        if cellar_wine:
            data = self.get_small_data()
            data['number'] = cellar_wine.get_small_data()['number']
            return data
        else:
            return None
    
    def get_data_number_area(self,cellar_id):
        data = self.get_data_number(cellar_id)
        data['winery_name']=self.winery.name
        data['area_name']=self.winery.area.name
        return data

    def get_data_number_trend(self,cellar_id):
        data = self.get_data_number(cellar_id)
        data['trend'] = self.get_trend()
        data['winery_name'] = self.winery.name
        return data

    def get_data_names(self):
        data = self.get_small_data()
        data['winery_name'] = self.winery.get_small_data()['name']
        return data

    def get_wine_detail(self, cellar_id):
        data = self.get_data_number(cellar_id)
        winery = Winery.get_by_id(self.winery).get_small_data()
        for key in winery.keys():
            data['winery_'+key] = winery[key]
        area = Area.get_by_id(winery['area']).get_info_data()
        for key in area.keys():
            data['area_'+key] = area[key]
        return data

    def modify_color(self):
        if self.color=='Blanc':
            return Wine.update(color='blanc').where(Wine.id==self.id).execute()
        elif self.color=='Rouge':
            return Wine.update(color='rouge').where(Wine.id==self.id).execute()
        elif self.color=='Rose':
            return Wine.update(color='rosé').where(Wine.id==self.id).execute()
        elif self.color=='Jaune':
            return Wine.update(color='jaune').where(Wine.id==self.id).execute()

class CellarWine(BaseModel):
    id = AutoField()
    cellar = ForeignKeyField(Cellar, backref='wines')
    wine = ForeignKeyField(Wine, backref='cellars')
    number = IntegerField()

    def modify_number(self, number):
        return CellarWine.update(number=self.number+number).where(CellarWine.cellar==self.cellar,CellarWine.wine==self.wine).execute()

    def get_vintage_number(self):
        data = self.get_small_data()
        data['vintage'] = self.wine.get_small_data()['vintage']
        return data
    
    def update_number(self, number):
        if self.number+number==0:
            return self.delete_instance()
        else:
            return CellarWine.update(number=self.number+number).where(CellarWine.cellar==self.cellar,CellarWine.wine==self.wine).execute()

with db:
    #migrate(migrator.drop_column('wine','advise',Wine.advise))
    #migrate(migrator.add_column('wine','advise',Wine.advise))
    Wine.create_table(safe=True)
    CellarWine.create_table(safe=True)