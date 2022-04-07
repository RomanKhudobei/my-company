from marshmallow import ValidationError

from app.exceptions.exceptions import APIException
from app.exceptions.handlers import validation_error_handler, api_exception_handler


def init_package(app):
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(APIException, api_exception_handler)


__all__ = (
    'init_package',
    'APIException',
)
