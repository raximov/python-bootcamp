from marshmallow import Schema, fields, validate

class CreateGameRequest(Schema):
    opponent = fields.Str(
        required=False,
        load_default="user",
        validate=validate.OneOf(["user", "computer"]),
    )

class MoveRequest(Schema):
    position = fields.Int(required=True, validate=validate.Range(min=1, max=9))
