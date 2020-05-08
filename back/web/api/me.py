from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.users import add_wine_to_cellar, get_user_by_id, get_my_wines, get_my_cellars, get_my_regions, get_my_areas, get_my_wineries
from back.controllers.cellars import create_cellar

from back.models import Wine
from back.models import User
from back.models import Cellar


class Me(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()['id']
        return get_user_by_id(user_id)

class MyCellar(Resource):
    # @jwt_required
    def get(self):
        return get_my_wines(request.headers['current_cellar_id'])
    
    @jwt_required
    def post(self):
        post_data = request.get_json()
        print(post_data)
        cellar = Cellar.get_by_id(post_data['cellar_id'])
        return add_wine_to_cellar(cellar=cellar, **post_data)

class MyCellars(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()['id']
        to_send = {'msg':'success'}
        cellars = get_my_cellars(user_id)
        if cellars == []:
            to_send['cellars'] = 'no registered cellar'
        else:
            to_send['cellars'] = cellars
        return to_send

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()['id']
        post_data = request.get_json()
        return create_cellar(user=user_id, name=post_data['name'])
        
class MyRegions(Resource):
    @jwt_required
    def get(self):
        cellar_id = request.headers['current_cellar_id']
        return get_my_regions(cellar_id)

class MyAreas(Resource):
    @jwt_required
    def get(self, region_id):
        cellar_id = request.headers['current_cellar_id']
        return get_my_areas(region_id, cellar_id)

class MyWineries(Resource):
    @jwt_required
    def get(self, area_id):
        cellar_id = request.headers['current_cellar_id']
        return get_my_wineries(area_id, cellar_id)

class MyWines(Resource):
    @jwt_required
    def get(self, winery_id):
        cellar_id = request.headers['current_cellar_id']
        return get_my_wines(winery_id, cellar_id)