"""Shoot view"""

from flask import request
from flask_restplus import Resource
from main import endpoint
from src.decorators.id_validation import validate_id
from src.helpers.response import ResponseHandler
from src.models import Shoot
from src.schemas.shoot import ShootListSchema


@endpoint('/shoot')
class ShootListView(Resource):
    """Shoot List/Create view"""
    def get(self):
        """Get request"""

        schema = ShootListSchema()
        shoots = Shoot.query.all()
        resp = schema.dump(shoots, many=True)
        response = ResponseHandler(data=resp).get_response()
        return response

    def post(self):
        """Add new shoot"""

        schema = ShootListSchema()
        shoot = schema.load(request.get_json())
        shoot.save()

        resp = schema.dump(shoot)
        response = ResponseHandler(msg_key='SYS_001',
                                   data=resp,
                                   status_code=201).get_response()
        return response


@endpoint('/shoot/<string:shoot_id>')
class ShootDetailView(Resource):
    """Shoot Detail/Patch view"""
    @validate_id
    def get(self, shoot_id):
        """Get a single shoot"""

        schema = ShootListSchema()
        shoot = Shoot.get(shoot_id)
        if shoot:
            resp = schema.dump(shoot)
            response = ResponseHandler(data=resp).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response

    @validate_id
    def patch(self, shoot_id):
        """Update a single shoot"""

        schema = ShootListSchema()
        schema.__model__ = None
        req_data = schema.load(request.get_json(), partial=True)

        shoot = Shoot.get(shoot_id)
        if shoot:
            shoot.update(**req_data)

            resp = schema.dump(shoot)
            response = ResponseHandler(msg_key='SYS_003',
                                       data=resp,
                                       status_code=200).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response

    @validate_id
    def delete(self, shoot_id):
        """Delete a single shoot"""

        schema = ShootListSchema()
        shoot = Shoot.get(shoot_id)
        if shoot:
            resp = schema.dump(shoot)
            shoot.delete()
            response = ResponseHandler(data=resp,
                                       msg_key='SYS_002',
                                       status_code=200).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response
