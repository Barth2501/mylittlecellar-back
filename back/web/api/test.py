from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.search_engine import main as search_engine


class Test(Resource):
    def get(self):
        query = "Vin de Pays de L'Herault"
        result = search_engine.find_area(query)
        return result