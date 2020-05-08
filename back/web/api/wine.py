from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.wines import search_wines, get_wine, search_other_vintage, search_other_wines, get_wine_trend


class Wines(Resource):
    @jwt_required
    def get(self):
        cellar_id = request.headers['current_cellar_id']
        query = request.args['query']
        to_send = {'msg':'success'}
        to_send['wines'] = search_wines(cellar_id, query)
        return to_send

    def post(self):
        pass

class Wine(Resource):
    @jwt_required
    def get(self, wine_id):
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['wine'] = get_wine(wine_id, cellar_id)
        return to_send

    def post(self, wine_id):
        pass

class WineVintage(Resource):
    @jwt_required
    def get(self, wine_id):
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['vintage'] = search_other_vintage(wine_id,cellar_id)
        return to_send

class WineOther(Resource):
    @jwt_required
    def get(self,wine_id):
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['wines'] = search_other_wines(wine_id,cellar_id)
        return to_send

class WineTrend(Resource):
    @jwt_required
    def get(self,wine_id):
        to_send = {'msg':'success'}
        to_send['trend'] = get_wine_trend(wine_id)
        return to_send