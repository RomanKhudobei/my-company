from flask import Blueprint
from flask_restful import Api

from company.resources.company import CompanyCreate, CompanyRetrieve, CompanyUpdate
from company.resources.employee import EmployeeCreate, EmployeeList

bp = Blueprint('company', __name__)
api = Api(bp)

api.add_resource(CompanyCreate, '/companies/', endpoint='create')
api.add_resource(CompanyRetrieve, '/companies/<int:company_id>/', endpoint='retrieve')
api.add_resource(CompanyUpdate, '/companies/<int:company_id>/', endpoint='update')

api.add_resource(EmployeeCreate, '/companies/<int:company_id>/employees/', endpoint='employee_create')
api.add_resource(EmployeeList, '/companies/<int:company_id>/employees/', endpoint='employee_list')
