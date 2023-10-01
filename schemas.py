from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Str()
    user_id = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    ign = fields.Str(required=True)

class UpdateUserSchema(Schema):
    username = fields.Str()
    password = fields.Str(required=True, load_only=True)
    new_password  = fields.Str()
    email = fields.Str()
    ign = fields.Str()

class DeleteUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)