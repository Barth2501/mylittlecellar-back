from flask import request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource


class CurrentCellar(Resource):
    @jwt_required
    def post(self):
        post_data = request.get_json()
        current_cellar = post_data['cellar_id']
        return {'msg':'updated'}