from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    _id = fields.String(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=2))
    last_name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    cpf = fields.String(
        required=True,
        validate=validate.Regexp(r'^\d{11}$', error="CPF deve conter exatamente 11 números.")
    )
    role = fields.String(required=True, validate=validate.OneOf(["admin", "patient"]))
    active = fields.Boolean(default=False)
    confirmation_code = fields.String(dump_only=True)

    class Meta:
        ordered = True
