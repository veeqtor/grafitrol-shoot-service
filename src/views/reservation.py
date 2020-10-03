from flask import request
from flask_restplus import Resource
from sqlalchemy.orm import joinedload

from main import endpoint
from src.decorators.id_validation import validate_id
from src.helpers.messages import ERROR_MSG
from src.helpers.response import ResponseHandler
from src.models import Reservation
from src.models.reservations import ReservationStatusChoices
from src.schemas.reservation import ReservationSchema
from utils.exceptions import ResponseException


@endpoint('/reservation')
class ReservationListView(Resource):
    """Reservation List/Create view"""
    def get(self):
        """Get request"""

        schema = ReservationSchema()
        reservations = Reservation.query.options(
            joinedload(Reservation.coordinator),
            joinedload(Reservation.shoot)).all()
        resp = schema.dump(reservations, many=True)
        response = ResponseHandler(data=resp).get_response()
        return response

    def post(self):
        """Create a new reservation"""

        schema = ReservationSchema()
        reservation = schema.load(request.get_json())
        reservation.save()
        resp = schema.dump(reservation)
        response = ResponseHandler(msg_key='SYS_001',
                                   data=resp,
                                   status_code=201).get_response()
        return response


@endpoint('/reservation/<string:reservation_id>')
class ReservationDetailView(Resource):
    """Reservation Detail/Patch view"""
    @validate_id
    def get(self, reservation_id):
        """Get a single reservation"""

        schema = ReservationSchema()
        reservation = Reservation.get_or_404(reservation_id)

        resp = schema.dump(reservation)
        response = ResponseHandler(data=resp).get_response()
        return response

    @validate_id
    def patch(self, reservation_id):
        """Update a reservation status"""

        schema = ReservationSchema()
        schema.__model__ = None
        req_data = schema.load(request.get_json(), partial=True)
        reservation = Reservation.get_or_404(reservation_id)
        statuses = [
            ReservationStatusChoices.cancelled,
            ReservationStatusChoices.completed
        ]
        if reservation.status in statuses:
            raise ResponseException(ERROR_MSG['RES_002'], 400)
        reservation.update(**req_data)
        resp = schema.dump(reservation)
        response = ResponseHandler(msg_key='SYS_003',
                                   data=resp,
                                   status_code=200).get_response()
        return response
