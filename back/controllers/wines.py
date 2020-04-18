from back.models.wine import Wine
from back.models.winery import Winery
from back.models.area import Area
from back.models.cellar import Cellar

from .wineries import create_winery
from .search_engine import main as search_engine
from .utils import df_to_dict, df_to_multi_index_dict

import requests
import os 
import pandas as pd


def create_wine(name:str, vintage:int, mark:int, number:int, maturity:str, winery_name:str):
    # wine_data = get_wine_from_hachette(payload)
    winery = Winery.get_or_none(name=winery_name)
    if not winery:
        # if 'winery_description' not in wine_data.keys():
        #     wine_data['winery_description'] = ''
        area_id = search_engine.find_area(name)
        area = Area.get_by_id(area_id)
        winery = create_winery(name=winery_name, area=area)
    #TODO mark, advise
    wine = Wine.create(winery=winery, name=name, vintage=vintage, mark=mark, advise=maturity)
    return wine

def region_agg(cellar_id:int):
    cellar = Cellar.get_by_id(cellar_id)
    wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
    wines=pd.DataFrame(wines)
    if 'region_name' not in wines.columns:
        return {'msg':'no wines in the cellar'}
    else:
        region_agg_df = wines.groupby('region_name').agg({'number':'sum'}).reset_index()
    return region_agg_df.to_dict('records')

def area_agg(cellar_id:int):
    cellar = Cellar.get_by_id(cellar_id)
    wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
    wines=pd.DataFrame(wines)
    if 'region_name' not in wines.columns:
        return {'msg':'no wines in the cellar'}
    else:
        area_agg_df = wines.groupby(['region_name','area_name']).agg({'number':'sum'}).reset_index().set_index('region_name')
    return df_to_multi_index_dict(area_agg_df)

def vintage_agg(cellar_id:int):
    cellar = Cellar.get_by_id(cellar_id)
    wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
    wines=pd.DataFrame(wines)
    if 'region_name' not in wines.columns:
        return {'msg':'no wines in the cellar'}
    else:
        vintage_agg_df = wines.groupby('vintage').agg({'number':'sum'}).reset_index()
        region_vintage_agg_df = wines.groupby(['region_name','vintage']).agg({'number':'sum'}).reset_index().set_index('region_name')
        area_vintage_agg_df = wines.groupby(['area_name','vintage']).agg({'number':'sum'}).reset_index().set_index('area_name')
    return vintage_agg_df.to_dict('records'), df_to_multi_index_dict(region_vintage_agg_df), df_to_multi_index_dict(area_vintage_agg_df)
