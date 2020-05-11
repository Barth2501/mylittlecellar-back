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
        wines = Wine.select()
        for i,wine in enumerate(wines):
            print(i)
            wine.modify_color()
        return {'msg':'done'}
