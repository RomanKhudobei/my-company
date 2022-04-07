from flask import Blueprint
from flask_restful import Api

from auth.resources import Login, RefreshToken

bp = Blueprint('auth', __name__)
api = Api(bp)

api.add_resource(Login, '/login/', endpoint='login')
api.add_resource(RefreshToken, '/token/refresh/', endpoint='refresh-token')
