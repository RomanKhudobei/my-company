from app.marshmallow import ma
from company.models import Company


class CompanySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Company
