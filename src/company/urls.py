from flask import Blueprint
from flask_restful import Api

from company.resources.company import CompanyCreate, CompanyRetrieve, CompanyUpdate
from company.resources.employee import EmployeeCreate

bp = Blueprint('company', __name__)
api = Api(bp)

api.add_resource(CompanyCreate, '/company/', endpoint='create')
api.add_resource(CompanyRetrieve, '/company/<int:company_id>/', endpoint='retrieve')
api.add_resource(CompanyUpdate, '/company/<int:company_id>/', endpoint='update')

api.add_resource(EmployeeCreate, '/company/<int:company_id>/employee/', endpoint='employee_create')
