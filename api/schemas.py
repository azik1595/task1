from marshmallow import Schema, fields, validates_schema, ValidationError


class AuthRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    surname  = fields.Str(required=True)
    @validates_schema
    def validate_lenght(self, data):
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']
            if len(username) > 30 or len(username) < 5:
                raise ValidationError(
                    'Username must be between 5 and 30 characters.',
                    'username')
            if len(password) > 30 or len(password) < 5:
                raise ValidationError(
                    'Password must be between 5 and 30 characters.',
                    'password')

    class Meta:
        ordered = True


class UserRegistrationRequestSchema(AuthRequestSchema):
    pass


class UserLoginRequestSchema(AuthRequestSchema):
    pass


class UserLoginResponseSchema(Schema):
    token = fields.Str()


class UserRegistrationResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()

    class Meta:
        ordered = True

        
class EventCouponSchema(Schema):
    event_id = fields.Int(required=True)
 
