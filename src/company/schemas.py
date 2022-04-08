from marshmallow import fields

from app.marshmallow import ma
from common.marshmallow_validators import not_empty
from company.models import Company


class CompanySchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=[not_empty])

    class Meta:
        model = Company
