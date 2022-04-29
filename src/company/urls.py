from flask import Blueprint
from flask_restful import Api

from company.resources.company import CompanyCreate, CompanyRetrieve, CompanyUpdate
from company.resources.employee import EmployeeCreate, EmployeeList, EmployeeRetrieve, EmployeeUpdate, EmployeeDelete
from company.resources.office import OfficeCreate, OfficeList, OfficeRetrieve, OfficeUpdate, OfficeDelete

bp = Blueprint('company', __name__)
api = Api(bp)

api.add_resource(CompanyCreate, '/companies/', endpoint='create')
api.add_resource(CompanyRetrieve, '/companies/<int:company_id>/', endpoint='retrieve')
api.add_resource(CompanyUpdate, '/companies/<int:company_id>/', endpoint='update')

api.add_resource(EmployeeCreate, '/companies/<int:company_id>/employees/', endpoint='employee_create')
api.add_resource(EmployeeList, '/companies/<int:company_id>/employees/', endpoint='employee_list')
api.add_resource(EmployeeRetrieve, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_retrieve')
api.add_resource(EmployeeUpdate, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_update')
api.add_resource(EmployeeDelete, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_delete')

api.add_resource(OfficeCreate, '/companies/<int:company_id>/offices/', endpoint='office_create')
api.add_resource(OfficeList, '/companies/<int:company_id>/offices/', endpoint='office_list')
api.add_resource(OfficeRetrieve, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_retrieve')
api.add_resource(OfficeUpdate, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_update')
api.add_resource(OfficeDelete, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_delete')
