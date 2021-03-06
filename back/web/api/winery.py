from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.wineries import get_winery_info
from back.controllers.areas import get_area_info, get_region_info, search_regions_areas


class Wineries(Resource):
    def get(self):
        pass

    def post(self):
        pass

class Area(Resource):
    @jwt_required
    def get(self, area_name):
        cellar_id = int(request.headers['current_cellar_id'])
        return get_area_info(area_name, cellar_id)

class Region(Resource):
    # @jwt_required
    def get(self, region_name):
        cellar_id = int(request.headers['current_cellar_id'])
        return get_region_info(region_name, cellar_id)

class Winery(Resource):
    @jwt_required
    def get(self, winery_id):
        cellar_id = int(request.headers['current_cellar_id'])
        return get_winery_info(winery_id, cellar_id)

    def post(self):
        pass

class RegionsAreas(Resource):
    @jwt_required
    def get(self):
        query = request.args['query']
        return search_regions_areas(query)
        