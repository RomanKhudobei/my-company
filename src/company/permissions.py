from functools import wraps

from flask_jwt_extended import current_user
from flask_restful import abort

from app.exceptions.exceptions import APIPermissionError
from company import services


def company_owner(parameter_name):
    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            assert current_user, '"jwt_required" decorator must be above this decorator'

            company_id = kwargs.get(parameter_name)
            company = services.get_company_by_id(company_id)

            if company is None:
                abort(404)

            if current_user.id != company.owner_id:
                raise APIPermissionError('You are not company owner')

            return f(*args, **kwargs)

        return decorated_function
    return decorator
