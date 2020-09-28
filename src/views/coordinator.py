"""Coordinator view"""

from dateutil import parser
from dateutil.parser import ParserError
from flask import request
from flask_restplus import Resource
from sqlalchemy.orm import joinedload

from main import endpoint
from src.decorators.validate_id import validate_id
from src.helpers.messages import ERROR_MSG
from src.helpers.response import ResponseHandler
from src.helpers.shoots_slots import get_preferred_coordinator
from src.models import Coordinator
from src.schemas.coordinator import CoordinatorSchema, CoordinatorListSchema
from utils.exceptions import ResponseException


@endpoint('/coordinator')
class CoordinatorListView(Resource):
    """Coordinator List/Create view"""
    def get(self):
        """Get Request"""
        selected_date = request.args.get('date')
        if selected_date:
            try:
                parser.parse(selected_date).date()
                schema = CoordinatorSchema()
                coordinators = Coordinator.query.options(
                    joinedload(Coordinator.reservations)).all()

                preferred = get_preferred_coordinator(coordinators,
                                                      selected_date)

                if preferred:
                    schema.context = {"timeslots": preferred[1]}
                    resp = schema.dump(preferred[0])
                    response = ResponseHandler(data=resp).get_response()
                    return response

                response = ResponseHandler(status='error',
                                           msg_key='CO_001',
                                           status_code=400).get_response()
                return response
            except ParserError:
                raise ResponseException(ERROR_MSG['SYS_003'], 400)
        else:
            schema = CoordinatorListSchema()
            coordinators = Coordinator.query.all()
            resp = schema.dump(coordinators, many=True)
            response = ResponseHandler(data=resp).get_response()
            return response

    def post(self):
        """Add a new coordinator"""

        schema = CoordinatorListSchema()
        coordinator = schema.load(request.get_json())
        coordinator.save()
        resp = schema.dump(coordinator)
        response = ResponseHandler(msg_key='SYS_001',
                                   data=resp,
                                   status_code=201).get_response()
        return response


@endpoint('/coordinator/<string:coordinator_id>')
class CoordinatorDetailView(Resource):
    """Coordinator Detail/Patch view"""
    @validate_id
    def get(self, coordinator_id):
        """Get a single coordinator"""

        schema = CoordinatorListSchema()
        coordinator = Coordinator.get(coordinator_id)
        if coordinator:
            resp = schema.dump(coordinator)
            response = ResponseHandler(data=resp).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response

    @validate_id
    def patch(self, coordinator_id):
        """Update a single coordinator"""

        schema = CoordinatorListSchema()
        schema.__model__ = None
        req_data = schema.load(request.get_json(), partial=True)

        coordinator = Coordinator.get(coordinator_id)
        if coordinator:
            coordinator.update(**req_data)

            resp = schema.dump(coordinator)
            response = ResponseHandler(msg_key='SYS_003',
                                       data=resp,
                                       status_code=200).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response

    @validate_id
    def delete(self, coordinator_id):
        """Delete a single coordinator"""

        schema = CoordinatorListSchema()
        coordinator = Coordinator.get(coordinator_id)
        if coordinator:
            resp = schema.dump(coordinator)
            coordinator.delete()
            response = ResponseHandler(data=resp,
                                       msg_key='SYS_002',
                                       status_code=200).get_response()
            return response
        response = ResponseHandler(status='error',
                                   msg_key='SYS_007',
                                   status_code=404).get_response()
        return response
