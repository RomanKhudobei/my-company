from app.db import db
from company.models import Company
from company.schemas import CompanySchema


def register_company(user, name):
    validated_data = CompanySchema(partial=True).load({'name': name})

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
    validated_data = CompanySchema().load(updated_data)

    for field, value in validated_data.items():
        setattr(company, field, value)

    db.session.commit()
