"""Shoot Schema"""

from marshmallow import fields
from src.models import Shoot
from src.schemas.base import BaseSchema
from src.schemas.fields import StringField
from src.schemas.reservation import ReservationSchema


class ShootListSchema(BaseSchema):
    """Shoot list schema"""

    __model__ = Shoot

    name = StringField(min_length=3,
                       max_length=50,
                       capitalize=True,
                       required=True)
    description = fields.String()
    price = fields.Float(required=True)
    duration = fields.Integer(required=True)


class ShootDetailWithReservationSchema(ShootListSchema):
    """Shoot detail with reservation schema"""
    reservations = fields.Nested(ReservationSchema(many=True))
