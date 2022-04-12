

class APIException(Exception):
    status_code = 500
    description = 'Server error occurred.'

    def __init__(self, description=None, **extra_kwargs):
        if description is not None:
            self.description = description

        self.extra_kwargs = extra_kwargs

    def as_dict(self):
        return {
            **self.extra_kwargs,
            'message': self.description
        }


class APIPermissionError(APIException):
    status_code = 403
    description = 'You don\'t have access permission.'
