from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from peewee import fn
from back.controllers.search_engine import main as search_engine
from back.models import *
from back.controllers.users import *
from back.controllers.wines import *
from back.controllers.recipes import *
from back.controllers.aging_model.aging_model import import_csv
class Test(Resource):
    def get(self):
        # query = "Champagne Brut Blanc de Blancs cuvee de la Table Ronde NV"
        # result = search_engine.find_area(query)
        # Winery.drop_table(cascade=True)
        # Wine.drop_table(cascade=True)
        # CellarWine.drop_table(cascade=True)
        # for i in range(1,10):
        #     cellar = Cellar.get_by_id(i)
        #     wines = Wine.select().from_(CellarWine, Wine).where(
        #                     CellarWine.wine==Wine.id,
        #                     CellarWine.cellar==cellar.id
        #     )
        #     for j, wine in enumerate(wines):
        #         cellar_wine=CellarWine.get_or_none(cellar=cellar, wine=wine)
        #         winery = Winery.get_by_id(wine.winery)
        #         cellar_winery = CellarWinery.get_or_none(cellar=cellar, winery=winery)
        #         if not cellar_winery:
        #             CellarWinery.create(cellar=cellar, winery=winery)
        #         area = Area.get_by_id(winery.area)
        #         cellar_area = CellarArea.get_or_none(cellar=cellar,area=area)
        #         if not cellar_area:
        #             CellarArea.create(cellar=cellar, area=area)
        #         region = Region.get_by_id(area.region)
        #         cellar_region = CellarRegion.get_or_none(cellar=cellar, region=region)
        #         if not cellar_region:
        #             CellarRegion.create(cellar=cellar, region=region)    
        #         cellar_winery.modify_number(cellar_wine.number)
        #         cellar_region.modify_number(cellar_wine.number)
        #         cellar_area.modify_number(cellar_wine.number)
        #         print('----------{}----------'.format(j))
        # id = [i for i in range(1,2)]
        # for i in id:
        #     area_vintage = AreaVintage.get_by_id(i)
        #     text = str(area_vintage.vintage).replace("'",'"').split("},{")
        #     res = {}
        #     for i,t in enumerate(text):
        #         if i==0:
        #             true = json.loads(t+'}')
        #         elif i == len(text)-1:
        #             true = json.loads('{'+t[:-1])
        #         else:
        #             true = json.loads('{'+t+'}')
        #         res[true['vintage'].strip()]=true['rank']
        #     res = str(res).replace("'",'"')
        #     AreaVintage.update(vintage='a').where(AreaVintage.id==i).execute()
        return import_csv()
