from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from back.controllers.wines import region_agg,area_agg, vintage_agg


class RegionStat(Resource):
    # @jwt_required
    def get(self):
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['region_agg'] = region_agg(cellar_id)
        return to_send

class AreaStat(Resource):
    # @jwt_required
    def get(self,region_name):
        print(region_name)
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['area_agg'] = area_agg(cellar_id, region_name)
        return to_send

class VintageStat(Resource):
    # @jwt_required
    def get(self, name):
        cellar_id = request.headers['current_cellar_id']
        to_send = {'msg':'success'}
        to_send['vintage_agg'] = vintage_agg(cellar_id, name)
        return to_send


