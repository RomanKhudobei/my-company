import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from common.marshmallow_validators import not_empty
from company.models import Company
from user.models import User


class CompanySchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=[not_empty])
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Company
        include_fk = True

    @validates('owner_id')
    def validate_owner(self, owner_id):
        owner = self.context.get('owner') or User.query.filter_by(id=owner_id).one_or_none()

        assert owner.id == owner_id, 'You must pass the same user to context as you pass id to load'

        if owner.employer is not None:
            raise marshmallow.ValidationError(
                message='Employee cannot create his own company',
                field_name='owner_id',
            )

        if owner.company is not None:
            raise marshmallow.ValidationError(
                message='User already have a company',
                field_name='owner_id',
            )
