from flask import Blueprint
from flask_restful import Api

from company.resources.company import CompanyCreate, CompanyRetrieve, CompanyUpdate
from company.resources.employee import EmployeeCreate, EmployeeList, EmployeeRetrieve, EmployeeUpdate, EmployeeDelete, \
    EmployeeSetPassword
from company.resources.office import OfficeCreate, OfficeList, OfficeRetrieve, OfficeUpdate, OfficeDelete, \
    AssignEmployeeToOffice, MyOffice
from company.resources.vehicles import VehicleCreate, VehicleList, VehicleUpdate, VehicleRetrieve, VehicleDelete, \
    MyVehicles

bp = Blueprint('company', __name__)
api = Api(bp)

api.add_resource(CompanyCreate, '/companies/', endpoint='create')
api.add_resource(CompanyRetrieve, '/companies/<int:company_id>/', endpoint='retrieve')
api.add_resource(CompanyUpdate, '/companies/<int:company_id>/', endpoint='update')

api.add_resource(EmployeeCreate, '/companies/<int:company_id>/employees/', endpoint='employee_create')
api.add_resource(EmployeeList, '/companies/<int:company_id>/employees/', endpoint='employee_list')
api.add_resource(EmployeeRetrieve, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_retrieve')
api.add_resource(EmployeeUpdate, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_update')
api.add_resource(EmployeeSetPassword, '/companies/<int:company_id>/employees/<int:employee_id>/set-password/', endpoint='employee_set_password')
api.add_resource(EmployeeDelete, '/companies/<int:company_id>/employees/<int:employee_id>/', endpoint='employee_delete')

api.add_resource(OfficeCreate, '/companies/<int:company_id>/offices/', endpoint='office_create')
api.add_resource(OfficeList, '/companies/<int:company_id>/offices/', endpoint='office_list')
api.add_resource(OfficeRetrieve, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_retrieve')
api.add_resource(OfficeUpdate, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_update')
api.add_resource(OfficeDelete, '/companies/<int:company_id>/offices/<int:office_id>/', endpoint='office_delete')
api.add_resource(AssignEmployeeToOffice, '/companies/<int:company_id>/offices/<int:office_id>/assign-employee/', endpoint='office_assign_employee')
api.add_resource(MyOffice, '/my-office/', endpoint='my_office')

api.add_resource(VehicleCreate, '/companies/<int:company_id>/vehicles/', endpoint='vehicle_create')
api.add_resource(VehicleList, '/companies/<int:company_id>/vehicles/', endpoint='vehicle_list')
api.add_resource(VehicleRetrieve, '/companies/<int:company_id>/vehicles/<int:vehicle_id>/', endpoint='vehicle_retrieve')
api.add_resource(VehicleUpdate, '/companies/<int:company_id>/vehicles/<int:vehicle_id>/', endpoint='vehicle_update')
api.add_resource(VehicleDelete, '/companies/<int:company_id>/vehicles/<int:vehicle_id>/', endpoint='vehicle_delete')
api.add_resource(MyVehicles, '/my-vehicles/', endpoint='my_vehicles')
