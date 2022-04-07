from app.exceptions import APIException


class AuthenticationFailed(APIException):
    status_code = 401
