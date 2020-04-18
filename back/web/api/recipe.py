from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.recipes import import_recipes, modify_ingredients_list

class ImportRecipes(Resource):
    def get(self):
        return import_recipes()
        
    def post(self):
        pass

class ModifyIngRecipes(Resource):
    def get(self):
        return modify_ingredients_list()

class Recipe(Resource):
    def get(self, recipe_id):
        pass
    def post(self):
        pass
