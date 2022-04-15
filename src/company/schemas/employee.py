import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from company.models import Employee
from user.models import User
from user.schemas import UserSchema


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema(exclude=['company']), dump_only=True)

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
