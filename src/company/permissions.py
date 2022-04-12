from functools import wraps

from flask_jwt_extended import current_user
from flask_restful import abort

from app.exceptions.exceptions import APIPermissionError


def company_owner(parameter_name):
    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            assert current_user, '"jwt_required" decorator must be above this decorator'

            company_id = kwargs.get(parameter_name)

            if not current_user.company:
                abort(404)

            if current_user.company.id != company_id:
                raise APIPermissionError('You are not company owner')

            return f(*args, **kwargs)

        return decorated_function
    return decorator
