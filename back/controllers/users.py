import pandas as pd
import json
from flask import jsonify

from back.models.wine import Wine,CellarWine
from back.models.recipe import Recipe, WineRecipe
from back.models.winery import Winery
from back.models.user import User
from back.models.cellar import Cellar

from back.assets.scrapping import get_first_wine_from_hachette
from .wines import create_wine
from .recipes import update_recipe

#TODO gerer le probleme des vins non présents sur hachette
def add_wine_to_cellar(cellar, wine_name:str, winery_name:str, vintage:int=0, number:int=1, mark:int=None, maturity:str=None, **kwargs):
    
    # wine_data = get_first_wine_from_hachette({'query':wine_name})

    wine = Wine.get_or_none(name=wine_name, vintage=vintage)
    if not wine:
        wine = create_wine(name=wine_name, vintage=vintage, number=number, mark=mark, maturity=maturity, winery_name=winery_name)
        
        ## This part has been commented because the recipe are not linked to the wine itself anymore
        ## Now recipes are linked to areas
        # for i,_ in enumerate(data_recipes['recipes_names']):
        #     recipe = Recipe.get_or_none(name=data_recipes['recipes_names'][i])
        #     if recipe:
        #         recipe = update_recipe(recipe=recipe, url=data_recipes['recipes_urls'][i])
        #         WineRecipe.create(wine=wine, recipe=recipe)
    cellarwine = CellarWine.get_or_none(cellar=cellar, wine=wine)
    if cellarwine:
        if cellarwine.number + int(number) == 0:
            cellarwine.deleted_instance()
            return {'msg':'deleted'}
        else:
            cellarwine.modify_number(number=int(number))
            return {'msg':'updated'}
    else:
        CellarWine.create(cellar=cellar, wine=wine, number=number)
        return {'msg':'created'}

def get_user_by_id(user_id:int):
    user = User.get_by_id(user_id)
    return user.get_small_data()

def get_my_cellars(user_id:int):
    user = User.get_by_id(user_id)
    return [c.get_small_data() for c in user.cellars]

def get_my_wines(cellar_id:int):
    cellar = Cellar.get_by_id(cellar_id)
    wines = [w.wine.get_all_data_number(cellar.id) for w in cellar.wines]
    wines=pd.DataFrame(wines)
    if 'region_name' not in wines.columns:
        return {'msg':'no wines in the cellar'}
    grouped = wines.groupby(['region_name','area_name','winery_name','name','vintage']).agg({'number':'sum'})
    to_send = {'msg':'success'}
    to_send['my_wines'] = df_to_dict(grouped)
    return to_send

def df_to_dict(df):
    if df.ndim == 1:
        return df.to_dict()
    ret = {}
    for key in df.index.get_level_values(0):
        sub_df = df.xs(key)
        ret[key] = df_to_dict(sub_df)
    return ret