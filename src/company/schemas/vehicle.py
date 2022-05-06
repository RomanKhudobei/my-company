import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from common.marshmallow_validators import not_empty
from company.models import Vehicle, Office, Company
from company.schemas.office import OfficeSchema
from user.models import User
from user.schemas import UserSchema


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)

    name = fields.String(required=True, allow_none=False, validate=[not_empty])
    model = fields.String(required=True, allow_none=False, validate=[not_empty])
    licence_plate = fields.String(required=True, allow_none=False, validate=[not_empty])

    office = fields.Nested(OfficeSchema(exclude=['vehicles']), dump_only=True)
    driver = fields.Nested(UserSchema(exclude=['employer', 'company', 'vehicles']), dump_only=True)

    office_id = fields.Integer(required=False, allow_none=True, load_only=True)
    driver_id = fields.Integer(required=False, allow_none=True, load_only=True)

    class Meta:
        model = Vehicle
        include_fk = True
        # include_relationships = True
        exclude = ['company']

    @validates('company_id')
    def validate_company_id(self, company_id):
        company = self.context.get('company_id') or Company.query.filter_by(id=company_id).one_or_none()

        if company is None:
            raise marshmallow.ValidationError(
                message='Company does not exist',
                field_name='company_id',
            )

    @marshmallow.validates_schema(skip_on_field_errors=True)
    def validate(self, data, **kwargs):
        company_id = data.get('company_id')
        office_id = data.get('office_id')
        driver_id = data.get('driver_id')

        if office_id:
            office = Office.query.filter_by(id=office_id).one_or_none()

            if office is None:
                raise marshmallow.ValidationError(
                    message='Office does not exist',
                    field_name='office_id',
                )

            if office.company_id != company_id:
                raise marshmallow.ValidationError(
                    message='Office not belongs to company',
                    field_name='office_id',
                )

        if driver_id:
            user = User.query.filter_by(id=driver_id).one_or_none()

            if user is None:
                raise marshmallow.ValidationError(
                    message='User does not exist',
                    field_name='driver_id',
                )

            employer = user.employer
            if not user.employer or employer.company_id != company_id:
                raise marshmallow.ValidationError(
                    message='User is not employee',
                    field_name='driver_id',
                )
