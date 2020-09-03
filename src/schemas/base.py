"""Base schema"""

from marshmallow import Schema, EXCLUDE, post_load
from marshmallow.fields import String


class BaseSchema(Schema):
    """Base schema"""

    model = None
    id = String(dump_only=True)

    def response_data(self, obj, message=None):
        """Response data"""
        res_data = {'data': self.dump(obj)}

        if message:
            res_data['message'] = message

        return res_data

    @post_load
    def create_obj(self, data, **kwargs):
        """Create objects"""

        if self.model:
            return self.model(**data)
        return data

    class Meta:
        """Meta data"""
        unknown = EXCLUDE
        ordered = True
