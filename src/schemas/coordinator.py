"""Coordinator Schema"""

from marshmallow import fields
from src.models import Coordinator
from src.schemas.base import BaseSchema


class CoordinatorListSchema(BaseSchema):
    """Coordinator list schema"""

    __model__ = Coordinator

    start_of_day = fields.Time(data_key='startOfDay', required=True)
    end_of_day = fields.Time(data_key='endOfDay', required=True)
    break_start_time = fields.Time(data_key='breakStartTime', required=True)
    break_duration = fields.Integer(data_key='breakDuration', required=True)
    is_available = fields.Boolean(data_key='isAvailable')
    user = fields.String(required=True)
    reservations = fields.Nested('src.schemas.reservation.ReservationSchema',
                                 many=True,
                                 exclude=['coordinator'])


class CoordinatorSchema(CoordinatorListSchema):
    """Coordinator schema"""

    timeslots = fields.Method('get_available_timeslots')

    class Meta:
        """Meta class"""
        exclude = ['reservations']

    def get_available_timeslots(self, obj):
        """Gets the available slot."""
        return self.context['timeslots']
