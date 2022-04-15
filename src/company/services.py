from sqlalchemy import or_

from app.db import db
from company.models import Company, Employee
from company.schemas.company import CompanySchema
from company.schemas.employee import EmployeeSchema
from user.models import User
from user.schemas import UserSchema


def register_company(user, name):
    validated_data = CompanySchema(context={'owner': user}).load({
        'name': name,
        'owner_id': user.id,
    })

    company = Company(
        owner=user,
        name=validated_data.get('name'),
    )
    db.session.add(company)

    db.session.commit()
    return company


def get_company_by_id(company_id):
    return Company.query.filter_by(id=company_id).one_or_none()


def update_company(company, updated_data):
    validated_data = CompanySchema(exclude=['owner_id']).load(updated_data)

    for field, value in validated_data.items():
        setattr(company, field, value)

    db.session.commit()


def create_employee(company, user_id):
    validated_data = EmployeeSchema(context={'company': company}, partial=True).load({'user_id': user_id})

    employee = Employee(
        company_id=company.id,
        user_id=validated_data.get('user_id'),
    )
    db.session.add(employee)

    db.session.commit()
    return employee


def get_company_employees(company_id, search_query=None):
    query = Employee.query.join(User).filter(Employee.company_id == company_id)

    if search_query:
        query = query.filter(
            or_(
                User.first_name.contains(search_query),
                User.last_name.contains(search_query),
                User.email.contains(search_query),
            )
        )

    return query


def get_employee_by_id(employee_id):
    return Employee.query.join(User).filter(Employee.id == employee_id).one_or_none()


def update_employee(employee, updated_data):
    validated_data = UserSchema().load(updated_data)

    for field, value in validated_data.items():
        setattr(employee.user, field, value)

    db.session.commit()


def delete_employee(employee):
    db.session.delete(employee)
    db.session.commit()
