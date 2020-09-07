import re

from marshmallow import ValidationError, fields

from src.helpers.messages import ERROR_MSG


class StringField(fields.String):
    """
    Custom String fields
    """
    def __init__(self,
                 *args,
                 min_length=None,
                 max_length=None,
                 capitalize=False,
                 **kwargs):
        validator_list = (self._get_min_length_validator(min_length) +
                          self._get_max_length_validator(max_length) +
                          kwargs.pop('validate', []))
        self.capitalize = capitalize
        super().__init__(
            validate=validator_list,
            *args,
            **kwargs,
        )

    def _deserialize(self, value, attr, data, **kwargs):
        """This method is called when data is being loaded to python
        It removes the all surrounding spaces and changes double spaces
        to one space.
        Args:
            value: value send from user
            attr: the field name
            data:  The raw input data passed to the Schema.load.
            **kwargs: Field-specific keyword arguments.
        Returns:
            (str):  A deserialized value with no double-space
        """
        des_value = super()._deserialize(value, attr, data, **kwargs)

        des_value = re.sub("\\s{2,}", " ", des_value.strip())
        return des_value.capitalize() if self.capitalize else des_value

    @staticmethod
    def _get_min_length_validator(min_length):
        def _validator(data):
            if len(data) < min_length:
                raise ValidationError(
                    message=ERROR_MSG['SYS_004'].format(min_length))

        return [_validator] if min_length else []

    @staticmethod
    def _get_max_length_validator(max_length):
        def _validator(data):
            if len(data) > max_length:
                raise ValidationError(
                    message=ERROR_MSG['SYS_005'].format(max_length))

        return [_validator] if max_length else []
