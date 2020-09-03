from marshmallow import fields
from src.models import User
from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    """User schema"""

    model = User
    name = fields.Str()
    email = fields.Str()
