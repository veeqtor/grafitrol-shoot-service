"""Reservation Schema"""

from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from src.decorators.id_validation import schema_id_validator
from src.helpers.messages import ERROR_MSG
from src.helpers.shoots_slots import is_duration_available
from src.models.reservations import ReservationStatusChoices
from src.schemas.base import BaseSchema
from src.schemas.fields import StringField
from src.models import Reservation, Coordinator, Shoot
from src.schemas.coordinator import CoordinatorListSchema
from src.schemas.shoot import ShootListSchema
from utils.datetime_helpers import convert_to_utc
from utils.exceptions import ResponseException


class ReservationSchema(BaseSchema):
    """Reservation schema"""

    __model__ = Reservation

    first_name = StringField(min_length=3,
                             max_length=100,
                             capitalize=True,
                             required=True,
                             data_key='firstName')
    last_name = StringField(min_length=3,
                            max_length=100,
                            capitalize=True,
                            required=True,
                            data_key='lastName')
    email = fields.Email(required=True)
    phone = StringField(min_length=10, max_length=100, required=True)
    additional_info = StringField(min_length=10,
                                  max_length=100,
                                  required=False,
                                  data_key='additionalInfo')
    status = EnumField(ReservationStatusChoices,
                       dump_by=EnumField.NAME,
                       load_by=EnumField.NAME)

    reservation_datetime = fields.DateTime(required=True,
                                           data_key='reservationDatetime')
    reservation_end_datetime = fields.Method('get_reservation_end_datetime',
                                             data_key='reservationEndDatetime',
                                             dump_only=True)
    duration = fields.Integer(required=True)

    coordinator_id = StringField(max_length=20,
                                 min_length=20,
                                 data_key='coordinatorId',
                                 load_only=True,
                                 validate=[schema_id_validator],
                                 required=True)
    shoot_id = StringField(max_length=20,
                           min_length=20,
                           data_key='shootId',
                           load_only=True,
                           validate=[schema_id_validator],
                           required=True)

    coordinator = fields.Nested(CoordinatorListSchema,
                                exclude=['reservations'],
                                dump_only=True)
    shoot = fields.Nested(ShootListSchema,
                          exclude=['reservations'],
                          required=True,
                          dump_only=True)

    def get_reservation_end_datetime(self, obj):
        """Get the reservation datetime"""
        return str(obj.reservation_end_datetime)

    @post_load
    def verify_duration_availability(self, data, **kwargs):
        """
		Verifies that the reservations duration is available for booking.
		"""
        statuses = [ReservationStatusChoices.cancelled]
        if kwargs.get('partial'):
            # TODO: Allow admins to change statuses
            if data.get('status') in statuses:
                return data
            raise ResponseException(ERROR_MSG['RES_002'], 401)
        else:
            coordinator = Coordinator.get_or_404(data.coordinator_id)
            shoot = Shoot.get_or_404(data.shoot_id)
            if shoot.duration != data.duration:
                raise ResponseException(ERROR_MSG['RES_003'], 400)
            start_datetime = convert_to_utc(data.reservation_datetime)
            end_datetime = convert_to_utc(data.reservation_end_datetime)
            date = start_datetime.strftime('%Y-%m-%d')
            slots = coordinator.get_slots_by_date(date)
            is_available = is_duration_available(start_datetime, end_datetime,
                                                 slots)
            if not is_available:
                raise ResponseException(ERROR_MSG['RES_001'], 400)
            return data
