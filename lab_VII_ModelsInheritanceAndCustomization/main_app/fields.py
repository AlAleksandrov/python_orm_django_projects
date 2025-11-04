from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, 'Available'),
            (False, 'Not Available')
        )
        kwargs['default'] = True
        super().__init__(*args, **kwargs)

class UnixTimeStampField(models.DateField):

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return datetime.fromtimestamp(value)

    def to_python(self, value):
        if isinstance(value, datetime):
            return value

        if value is None:
            return None

        return datetime.fromtimestamp(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return int(value.timestamp())

class PositiveIntegerField(models.IntegerField):
    def validate(self, value, model_instance):
        if value < 0:
            raise ValidationError('The value must be a positive integer')
        super().validate(value, model_instance)