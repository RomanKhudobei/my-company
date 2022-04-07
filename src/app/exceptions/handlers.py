import json

from flask import Response, jsonify
from marshmallow import ValidationError

from app.exceptions.exceptions import APIException


def validation_error_handler(e: ValidationError):
    return Response(
        response=json.dumps(e.messages),
        status=400,
        headers={'content-type': 'application/json'}
    )


def api_exception_handler(e: APIException):
    response = jsonify(e.as_dict())
    response.status_code = e.status_code
    return response
