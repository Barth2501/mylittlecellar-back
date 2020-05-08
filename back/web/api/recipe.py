from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.recipes import import_recipes, modify_ingredients_list, find_wines, find_recipes

class ImportRecipes(Resource):
    def get(self):
        return import_recipes()
        
    def post(self):
        pass

class ModifyIngRecipes(Resource):
    def get(self):
        return modify_ingredients_list()

class RecipesToWines(Resource):
    @jwt_required
    def post(self):
        post_data = request.get_json()
        to_send = {'msg':'success'}
        to_send['top_wines'],to_send['top_areas'] = find_wines(**post_data)
        return to_send

class WinesToRecipes(Resource):
    @jwt_required
    def get(self,wine_id):
        to_send = {'msg':'success'}
        to_send['top_recipes'] = find_recipes(wine_id)
        return to_send
