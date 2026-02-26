from marshmallow import Schema, fields

class JwtRequest(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)

class JwtResponse(Schema):
    token_type = fields.Str(dump_only=True, default="Bearer", data_key="type")
    access_token = fields.Str(dump_only=True, data_key="accessToken")
    refresh_token = fields.Str(dump_only=True, data_key="refreshToken")

class RefreshJwtRequest(Schema):
    refresh_token = fields.Str(required=True, data_key="refreshToken")
