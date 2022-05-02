import marshmallow
from marshmallow import fields, validates, validates_schema

from app.marshmallow import ma
from company.models import Employee, Office
from user.models import User
from user.schemas import UserSchema


class EmployeeCreateSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema(exclude=['company', 'employer']), dump_only=True)

    class Meta:
        model = Employee
        include_fk = True
        # include_relationships = True

    @validates('user_id')
    def validate_user_id(self, user_id):
        user = User.query.filter_by(id=user_id).one_or_none()

        if user is None:
            raise marshmallow.ValidationError(
                message='User does not exist.',
                field_name='user_id',
            )

        if user.employer is not None:
            raise marshmallow.ValidationError(
                message='User already employed',
                field_name='user_id',
            )

        if user.company is not None:
            raise marshmallow.ValidationError(
                message='Company owner cannot be registered as employee',
                field_name='user_id',
            )

        company = self.context.get('company')
        assert company, 'Company in context required'

        if company.owner_id == user.id:
            raise marshmallow.ValidationError(
                message='Owner of the company cannot be registered as employee',
                field_name='user_id',
            )


class AssignEmployeeToOfficeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer()

    class Meta:
        model = Employee
        include_fk = True
        exclude = ['user_id', 'created_at', 'company_id']

    @validates('office_id')
    def validate_office_id(self, office_id):
        office = self.context.get('office') or Office.query.filter_by(id=office_id).one_or_none()

        if office is None:
            raise marshmallow.ValidationError(
                message='Office does not exist',
                field_name='office_id',
            )

    @marshmallow.validates_schema(skip_on_field_errors=True)
    def validate(self, data, **kwargs):
        employee = self.context.get('employee') or Employee.query.filter_by(id=data['id'])
        assert employee.id == data['id'], 'Provided wrong employee to context'

        office = self.context.get('office') or Office.query.filter_by(id=data['office_id'])

        if employee.company_id != office.company_id:
            raise marshmallow.ValidationError(
                message='Employee is from another company',
                field_name='employee_id',
            )
