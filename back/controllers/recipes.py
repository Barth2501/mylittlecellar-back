import os
import requests
import json
import re
import pandas as pd

from back.models import *

import back.controllers.search_engine.main as search_engine
from back.controllers.utils import df_to_dict


def update_recipe(recipe, url:str):
    payload = {"url": url}
    if os.environ.get('USE_NGROK')=='True':
        recipe_data = requests.post(os.environ.get('NGROK_SCRAP') + '/hachette/recipe', json=payload)    
    else:
        recipe_data = requests.post('http://localhost:8001/hachette/recipe', json=payload)
    recipe_data = recipe_data.json()
    return recipe.update(ingredients=recipe_data['recipe_ingredients'], preparation=recipe_data['recipe_prepa'])

def import_recipes():
    Category.create(name='no category')
    page_index = [i for i in range(1,134)]
    for i in page_index:
        payload = {'index':i}
        if os.environ.get('USE_NGROK')=='True':
            recipes_data = requests.post(os.environ.get('NGROK_SCRAP') + '/hachette/recipes', json=payload)    
        else:
            recipes_data = requests.post('http://localhost:8001/hachette/recipes',json=payload)
        recipes_data = recipes_data.json()
        print('-----------{}---------------'.format(i))
        print(recipes_data['recipes'])
        for recipe_data in recipes_data['recipes']:
            if 'areas' in recipe_data.keys():
                if 'category_name' in recipe_data.keys():
                    category = Category.get_or_none(name=recipe_data['category_name'])
                    if not category:
                        category = Category.create(name=recipe_data['category_name'])
                else:
                    category = Category.get(name='no category')
                recipe = Recipe.get_or_none(name=recipe_data['name'])
                if not recipe:
                    recipe = Recipe.create(category=category, **recipe_data)
                for area_data in recipe_data['areas']:
                    area = Area.get_or_none(name=area_data)
                    if not area:
                        area = Area.create(name=area_data)
                    AreaRecipe.create(area=area, recipe=recipe)
    return {'msg':'success'}

def modify_ingredients_list():
    recipes = Recipe.select(Recipe.id, Recipe.name, Recipe.ingredients)
    for recipe in recipes:
        if not recipe.ingredients:
            recipe.modify_ing()
    return {'msg':'success'}

def find_wines(query:str, cellar, color=None, event=None, **kwargs):
    
    # on limite le nombre de recettes
    adv_recipes = search_engine.find_recipes(query, 'vectorial')[:5]
    adv_recipes_df = pd.DataFrame(adv_recipes,columns=['recipe_id','score'])
    # on ne peut pas limiter le nombre de visn retournés car ils ne sont pas triés
    # a l'avenir, une fois qu'on aura sauvergardé tous les scores dans chaque vins on pourra les trier par score décroissant
    recipes_list = list(map(lambda x: x[0],adv_recipes))
    relevant_wines = Wine.select(Wine.id, AreaRecipe.recipe.alias('recipe_id')).distinct().join(Winery, on=(Winery.id==Wine.winery).alias('winery')
                                ).join(Area, on=(Area.id==Winery.area).alias('area')
                                ).join(AreaRecipe, on=(AreaRecipe.area==Area.id).alias('arearecipe')
                                ).join(CellarWine, on=(CellarWine.wine==Wine.id)
                                ).where(AreaRecipe.recipe<<recipes_list, CellarWine.cellar==cellar).dicts()
    wines = []
    for wine in relevant_wines:
        print(wine)
        mat_score = Wine.get_by_id(wine['id']).get_trend()
        # gerer ici les vins dont le score de maturité n'a pas pu etre calculés
        if mat_score:
            mat_score = mat_score['value'][0]
            wines.append({"wine_id":wine['id'], "mat_score":mat_score, "recipe_id":wine['recipe_id']})
    wines_df = pd.DataFrame(wines)
    global_df = wines_df.merge(adv_recipes_df, how='inner', on="recipe_id")
    global_df['global_score'] = global_df.apply(lambda x: x['mat_score']*x['score'], axis=1)
    global_df = global_df.groupby('wine_id').agg({'global_score':'sum'}).sort_values('global_score', ascending=False).reset_index()

    top_wines = [Wine.get_by_id(wine.wine_id).get_data_number_area(cellar) for wine in global_df.head(5).itertuples()]

    # find the areas that also match
    relevant_areas = Area.select(Area, Region.name.alias('region_name'), CellarArea.number).distinct().join(AreaRecipe, on=(Area.id==AreaRecipe.area)
                        ).join(CellarArea, on=(CellarArea.area==Area.id)
                        ).join(Region, on=(Area.region==Region.id)).where(AreaRecipe.recipe<<recipes_list, CellarArea.cellar==cellar).dicts()
    top_areas = [{**area} for area in relevant_areas]
    return top_wines, top_areas
    # sel_recipes = Recipe.select().where(Recipe.id << recipes_list)
    # sel_areas = Recipe.select(
    #                     Area.name.alias('area_name'),
    #                     AreaRecipe.recipe.alias('recipe_id'),
    #                     CellarWine.number.alias('number'),
    #                     Wine.id.alias('wine_id'),
    #                     Winery.name.alias('winery_name'),
    #                     Region.name.alias('region_name')
    #                 ).from_(Area, AreaRecipe,CellarWine,Wine,Winery,Region).where(
    #                     Area.id==AreaRecipe.area,
    #                     AreaRecipe.recipe<<sel_recipes,
    #                     CellarWine.cellar==cellar,
    #                     CellarWine.wine==Wine.id,
    #                     Area.id==Winery.area,
    #                     Winery.id==Wine.winery,
    #                     Region.id==Area.region
    #                 ).dicts()
    # wines = []
    # for area in sel_areas:
    #     print(area)
    #     wines_dict={}
    #     for key in area.keys():
    #         if key != 'wine_id':
    #             wines_dict[key] = area[key]
    #     wine_info = Wine.get_by_id(area['wine_id']).get_small_data()
    #     for key in wine_info.keys():
    #         wines_dict[key] = wine_info[key]
    #     recipe_name = Recipe.get_by_id(area['recipe_id']).get_small_data()['name']
    #     wines_dict['recipe_name'] = recipe_name
    #     wines.append(wines_dict)
    # print(wines)
    # wines_df = pd.DataFrame(wines)
    # score_wines_df = pd.merge(wines_df, adv_recipes_df, on='recipe_id')
    
    # score_wines_df['color'] = score_wines_df.advise.map(lambda x: x.split('/')[0] if x else 'undefined')
    # score_wines_df['advise'] = score_wines_df.advise.map(lambda x: x.split('/')[1] if x else 'undefined')
    # score_wines_df = score_wines_df[score_wines_df.advise!='à garder']
    # if color:
    #     score_wines_df = score_wines_df[score_wines_df.color==color]
    # if event:
    #     score_wines_df = score_wines_df[score_wines_df.event==event]
    # score_wines_df = score_wines_df.fillna(0)

    # score_wines_df = score_wines_df.groupby(['region_name','area_name','number','winery_name','name','vintage','mark','advise']).agg({'score':'sum'}).reset_index()
    # top_wines_df = score_wines_df.sort_values(['score','mark'], ascending=False).head(5)
    
    # top_areas = score_wines_df.sort_values('score',ascending=False).groupby(['area_name','winery_name','name','vintage']).agg({'number':'sum'})
    
    return df_to_dict(top_wines_df), df_to_dict(top_areas)

def find_recipes(wine_id:int):
    wine = Wine.get_by_id(wine_id)
    winery = Winery.get_by_id(wine.winery)
    area = Area.get_by_id(winery.area)
    return [a.recipe.get_small_data() for a in area.recipes]