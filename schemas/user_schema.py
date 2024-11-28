from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    cpf = fields.String(required=True, validate=validate.Regexp(r'^\d{11}$'))