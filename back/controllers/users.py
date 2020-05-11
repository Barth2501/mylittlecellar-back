import pandas as pd
import json
from flask import jsonify
import time
from playhouse.shortcuts import model_to_dict

from back.models import *

from back.assets.scrapping import get_first_wine_from_hachette
from .wines import create_wine
from .recipes import update_recipe

# TODO gerer le probleme des vins non présents sur hachette


def add_wine_to_cellar(cellar, wine_name: str, winery_name: str, color: str, vintage: int = 0, number: int = 1, mark: int = None, maturity: str = None, **kwargs):

    # wine_data = get_first_wine_from_hachette({'query':wine_name})

    wine = Wine.get_or_none(name=wine_name, vintage=vintage, color=color)
    if not wine:
        wine = create_wine(name=wine_name, vintage=vintage, number=number,
                           mark=mark, maturity=maturity, winery_name=winery_name, color=color)
    # CellarWinery
    winery = Winery.get_by_id(wine.winery)
    cellar_winery = CellarWinery.get_or_none(cellar=cellar, winery=winery)
    if not cellar_winery:
        CellarWinery.create(cellar=cellar, winery=winery)
    else:
        cellar_winery.update_number(number=int(number))
    # CellarArea
    area = Area.get_by_id(winery.area)
    cellar_area = CellarArea.get_or_none(cellar=cellar,area=area)
    if not cellar_area:
        CellarArea.create(cellar=cellar, area=area)
    else:
        cellar_area.update_number(number=int(number))
    # CellarRegion
    region = Region.get_by_id(area.region)
    cellar_region = CellarRegion.get_or_none(cellar=cellar, region=region)
    if not cellar_region:
        CellarRegion.create(cellar=cellar, region=region)
    else:
        cellar_region.update_number(number=int(number))
    #CellarWine
    cellarwine = CellarWine.get_or_none(cellar=cellar, wine=wine)
    if cellarwine:
        cellarwine.update_number(numner=int(number))
        return {'msg':'updated'}
    else:
        CellarWine.create(cellar=cellar, wine=wine, number=number)
        return {'msg': 'created'}


def get_user_by_id(user_id: int):
    user = User.get_by_id(user_id)
    return user.get_small_data()


def get_my_cellars(user_id: int):
    user = User.get_by_id(user_id)
    return [c.get_small_data() for c in user.cellars]


# def get_my_wines(cellar_id: int):
#     cellar = Cellar.get_by_id(cellar_id)
#     start = time.time()
#     wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
#     print(time.time()-start)
#     wines = pd.DataFrame(wines)
#     print(time.time()-start)
#     if 'region_name' not in wines.columns:
#         return {'msg': 'no wines in the cellar'}
#     grouped = wines.groupby(
#         ['region_name', 'area_name', 'winery_name', 'name', 'vintage']).agg({'number': 'sum'})
#     print(time.time()-start)
#     to_send = {'msg': 'success'}
#     to_send['my_wines'] = df_to_dict(grouped)
#     return to_send

def get_my_regions(cellar_id:int):
    regions = Region.select().from_(Region,CellarRegion).where(
        CellarRegion.cellar==cellar_id,
        CellarRegion.region==Region.id
    )
    return { region.get_small_data()['id']:region.get_small_data() for region in regions}

def get_my_areas(region_id: int, cellar_id: int):
    areas = Area.select().from_(CellarArea, Area, Region).where(
        CellarArea.cellar==cellar_id,
        CellarArea.area==Area.id,
        Region.id==region_id,
        Area.region==Region.id
    )
    return {area.get_small_data()['id']:area.get_small_data() for area in areas}

def get_my_wineries(area_id:int, cellar_id:int):
    wineries = Winery.select(Winery, CellarWinery.number).join(
                        CellarWinery, on=(CellarWinery.winery==Winery.id)).join(
                        Area, on=(Area.id==Winery.area)).where(
                            Area.id==area_id,
                            CellarWinery.cellar==cellar_id).dicts()

    # wineries = Winery.select().from_(Winery,CellarWinery,Area).where(
    #     CellarWinery.cellar==cellar_id,
    #     Area.id==area_id,
    #     Winery.area==Area.id,
    #     CellarWinery.winery==Winery.id
    # )
    return {winery['id']:{'name':winery['name'], 'number':winery['number']} for winery in wineries}

def get_my_wines(winery_id:int, cellar_id:int):
    wine_q = Wine.select(Wine.name, Wine.vintage, CellarWine.number).join(
                        CellarWine, on=(CellarWine.wine==Wine.id)).join(
                        Winery, on=(Winery.id==Wine.winery)).where(
                        Winery.id==winery_id,
                        CellarWine.cellar==cellar_id).dicts()
    wines = [{'name':wine['name'], 'vintage':wine['vintage'], 'number':wine['number']} for wine in wine_q]
    # winery = Winery.get_by_id(winery_id)
    # wines = [wine.get_data_number(cellar_id) for wine in winery.wines]
    wines = pd.DataFrame(wines)
    grouped = wines.groupby(
         ['name', 'vintage']).agg({'number': 'sum'})
    return df_to_dict(grouped)

def df_to_dict(df):
    if df.ndim == 1:
        return df.to_dict()
    ret = {}
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        ret[key] = df_to_dict(sub_df)
    return ret
