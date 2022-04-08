from flask import Blueprint
from flask_restful import Api

from company.resources import CompanyCreate, CompanyRetrieve, CompanyUpdate

bp = Blueprint('company', __name__)
api = Api(bp)

api.add_resource(CompanyCreate, '/company/', endpoint='create')
api.add_resource(CompanyRetrieve, '/company/<int:company_id>/', endpoint='retrieve')
api.add_resource(CompanyUpdate, '/company/<int:company_id>/', endpoint='update')
