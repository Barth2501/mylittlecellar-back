from back.models import *
from playhouse.shortcuts import model_to_dict

from .wineries import create_winery
from .search_engine import main as search_engine
from .utils import df_to_dict, df_to_multi_index_dict

import requests
import os
import pandas as pd
from peewee import fn


def create_wine(name: str, vintage: int, mark: int, number: int, maturity: str, winery_name: str, color: str):
    # wine_data = get_wine_from_hachette(payload)
    winery = Winery.get_or_none(name=winery_name)
    if not winery:
        # if 'winery_description' not in wine_data.keys():
        #     wine_data['winery_description'] = ''
        area_id = search_engine.find_area(name)
        area = Area.get_by_id(area_id)
        winery = create_winery(name=winery_name, area=area)
    # TODO mark, advise
    wine = Wine.create(winery=winery, name=name, vintage=vintage,
                       mark=mark, advise=maturity, color=color)
    return wine

# def region_agg(cellar_id:int):
#     cellar = Cellar.get_by_id(cellar_id)
#     wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
#     wines=pd.DataFrame(wines)
#     if 'region_name' not in wines.columns:
#         return {'msg':'no wines in the cellar'}
#     else:
#         region_agg_df = wines.groupby('region_name').agg({'number':'sum'}).reset_index()
#     return region_agg_df.to_dict('records')


def region_agg(cellar_id: int):
    cellar = Cellar.get_by_id(cellar_id)
    return [c.get_region_number() for c in cellar.region]

# def area_agg(cellar_id:int):
#     cellar = Cellar.get_by_id(cellar_id)
#     wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
#     wines=pd.DataFrame(wines)
#     if 'region_name' not in wines.columns:
#         return {'msg':'no wines in the cellar'}
#     else:
#         area_agg_df = wines.groupby(['region_name','area_name']).agg({'number':'sum'}).reset_index().set_index('region_name')
#     return df_to_multi_index_dict(area_agg_df)


def area_agg(cellar_id: int, region_name: str):
    query = Area.select(Area.name, fn.Count(CellarArea.number).alias('number')).from_(Area, Region, CellarArea).where(
        CellarArea.cellar == cellar_id,
        Region.name == region_name,
        Area.region == Region.id,
        CellarArea.area == Area.id
    ).group_by(Area.name)
    return [{'area_name': i.name, 'number': i.number} for i in query.execute()]

# def vintage_agg(cellar_id:int):
#     cellar = Cellar.get_by_id(cellar_id)
#     wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
#     wines=pd.DataFrame(wines)
#     if 'region_name' not in wines.columns:
#         return {'msg':'no wines in the cellar'}
#     else:
#         vintage_agg_df = wines.groupby('vintage').agg({'number':'sum'}).reset_index()
#         region_vintage_agg_df = wines.groupby(['region_name','vintage']).agg({'number':'sum'}).reset_index().set_index('region_name')
#         area_vintage_agg_df = wines.groupby(['area_name','vintage']).agg({'number':'sum'}).reset_index().set_index('area_name')
#     return vintage_agg_df.to_dict('records'), df_to_multi_index_dict(region_vintage_agg_df), df_to_multi_index_dict(area_vintage_agg_df)


def vintage_agg(cellar_id: int, name: str):
    cellar = Cellar.get_by_id(cellar_id)
    region = Region.get_or_none(name=name)
    area = Area.get_or_none(name=name)
    if region:
        wines = Wine.select(Wine.vintage, fn.Count(CellarRegion.number).alias('number')).from_(Wine, CellarRegion, Region, Area, Winery).where(
            CellarRegion.cellar == cellar_id,
            Region.id == region,
            Region.id == Area.region,
            Winery.area == Area.id,
            Wine.winery == Winery.id,
            CellarRegion.region == region
        ).group_by(Wine.vintage).order_by(Wine.vintage)
        return [{'vintage': i.vintage, 'number': i.number} for i in wines.execute()]
    elif area:
        wines = Wine.select(Wine.vintage, fn.Count(CellarArea.number).alias('number')).from_(Wine, CellarArea, Area, Winery).where(
            CellarArea.cellar == cellar_id,
            Area.id == area,
            Winery.area == Area.id,
            Wine.winery == Winery.id,
            Area.id == CellarArea.area
        ).group_by(Wine.vintage).order_by(Wine.vintage)
        return [{'vintage': i.vintage, 'number': i.number} for i in wines.execute()]
    else:
        query = Wine.select(Wine.vintage, fn.Count(CellarWine.number).alias('number')).from_(Wine, CellarWine).where(
            Wine.id == CellarWine.wine,
            CellarWine.cellar == cellar
            ).group_by(Wine.vintage).order_by(Wine.vintage)
        return [{'vintage': i.vintage, 'number': i.number} for i in query.execute()]


def search_wines(cellar_id: int, query: str):
    wines_query = Wine.select(
        Wine.id, Wine.name, Wine.color, Wine.vintage, Winery.name
        ).join(Winery, on=(Winery.id == Wine.winery).alias('winery')
        ).join(CellarWine, on=(CellarWine.wine == Wine.id)).where(CellarWine.cellar == cellar_id).limit(10).distinct()
    for q in query.split(' '):
        wines_query=wines_query.where((Wine.name.contains(q) | Winery.name.contains(q)))
    return [{'id': i.id, 'name': i.name, 'color':i.color, 'vintage':i.vintage, 'winery_name': i.winery.name} for i in wines_query.execute()]

def get_wine(wine_id: int, cellar_id: int):
    wine=Wine.get_by_id(wine_id)
    return wine.get_wine_detail(cellar_id)

def search_other_vintage(wine_id: int, cellar_id: int):
    wine=Wine.get_by_id(wine_id)
    wines=Wine.select().from_(Wine, CellarWine, Winery).where(
        CellarWine.cellar == cellar_id,
        CellarWine.wine == Wine.id,
        Wine.id != wine_id,
        Wine.name == wine.name,
        Winery.id == wine.winery,
        Winery.id == Wine.winery
    )
    return [wine.get_data_number_trend(cellar_id) for wine in wines]

def search_other_wines(wine_id: int, cellar_id: int):
    wine=Wine.get_by_id(wine_id)
    wines=Wine.select().from_(CellarWine, Wine, Winery).where(
        CellarWine.cellar == cellar_id,
        CellarWine.wine == Wine.id,
        Wine.winery == Winery.id,
        Wine.winery == wine.winery,
        Wine.name != wine.name,
    )
    return [wine.get_data_number_trend(cellar_id) for wine in wines]

def get_wine_trend(wine_id: int):
    wine=Wine.get_by_id(wine_id)
    return wine.get_trend()

def get_wines_from_winery(winery_id:int,cellar_id:int):
    wines = Wine.select(Wine, CellarWine.number).join(
                CellarWine, on=(CellarWine.wine==Wine.id)).join(
                Winery, on=(Wine.winery==Winery.id)).where(
                CellarWine.cellar==cellar_id,
                Winery.id==winery_id).dicts()
    return [{**wine} for wine in wines]