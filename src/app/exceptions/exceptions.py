

class APIException(Exception):
    status_code = 500

    def __init__(self, description, **extra_kwargs):
        self.description = description
        self.extra_kwargs = extra_kwargs

    def as_dict(self):
        return {
            **self.extra_kwargs,
            'message': self.description
        }
