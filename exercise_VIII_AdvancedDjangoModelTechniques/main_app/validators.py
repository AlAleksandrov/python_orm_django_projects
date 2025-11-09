import re

from django.utils.deconstruct import deconstructible
from typing_extensions import Callable, Optional

from django.core.exceptions import ValidationError

# Option 1
# def validate_name(value: str) -> None:
#     for char in value:
#         if not (char.isalpha() or char.isspace()):
#             raise ValidationError("Name can only contain letters and spaces")

# Option 2
# def validate_name(message: str) -> Callable:
#     def validator(value: str) -> None:
#         for char in value:
#             if not (char.isalpha() or char.isspace()):
#                 raise ValidationError(message=message)
#
#     return validator

# Option 3
@deconstructible
class NameValidator:
    DEFAULT_MESSAGE: str = 'Name can only contain letters and spaces'

    def __init__(self, message: Optional[str]=None) -> None:
        self.message = message

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value) -> None:
        if not value:
            self.__message = self.DEFAULT_MESSAGE

        self.__message = value

    def __call__(self, value: str) -> None:
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(message=self.message)


@deconstructible
class PhoneNumberValidator:
    def __init__(self, message: str) -> None:
        self.message = message

    def __call__(self, value: str) -> None:
        if not re.match('^\+359\d{9}$',value):
            raise ValidationError(message=self.message)