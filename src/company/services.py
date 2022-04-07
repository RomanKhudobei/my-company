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
