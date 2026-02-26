from marshmallow import Schema, fields, validate, ValidationError

class SignUpRequest(Schema):
    login = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))

class LoginRequest(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)
