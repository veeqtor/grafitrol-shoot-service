from marshmallow import fields
from src.models import Reservation
from src.schemas.base import BaseSchema


class ReservationSchema(BaseSchema):
    """Reservation schema"""

    __model__ = Reservation

    first_name = fields.String()
    last_name = fields.String()
