"""Module to validate resource id from url parameters"""

import re
from functools import wraps
from marshmallow import ValidationError
from src.helpers.messages import ERROR_MSG


def is_id_valid(id_):
    """Check if id is valid"""
    return bool(re.match(r'^[\-a-zA-Z0-9_]{20}$', id_))


def validate_id(func):
    """Decorator function for views to validate id"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Function with decorated function mutations."""
        check_id_valid(**kwargs)
        return func(*args, **kwargs)

    return decorated_function


def check_id_valid(**kwargs):
    """Check if id is valid"""

    for key in kwargs:
        if key.endswith('_id') and not is_id_valid(kwargs.get(key, None)):
            raise ValidationError(ERROR_MSG['SYS_006'])
