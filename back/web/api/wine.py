from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource


class Wines(Resource):
    def get(self):
        pass

    def post(self):
        pass

class Wine(Resource):
    def get(self, wine_id):
        pass

    def post(self, wine_id):
        pass