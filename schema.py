from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields


class UserDetails(Schema):
    id = fields.Integer()
    username = fields.String(validate=validate.Length(min=1))
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    phone = fields.String()
    accessLevel = fields.String(validate=validate.OneOf(["admin", "passenger"]))


class UserQuery(Schema):
    username = fields.String(validate=validate.Length(min=1))
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    phone = fields.String()
    accessLevel = fields.String(validate=validate.OneOf(["admin", "passenger"]))


class OrderDetails(Schema):
    id = fields.Integer()
    carId = fields.Integer()
    userId = fields.Integer()
    shipDate = fields.Date()
    returnDate = fields.Date()
    status = fields.String(validate=validate.OneOf(["placed", "approved", "delivered"]))
    complete = fields.Boolean()


class OrderQuery(Schema):
    userId = fields.Integer()
    shipDate = fields.Date()
    returnDate = fields.Date()


class CarDetails(Schema):
    carId = fields.Integer()
    name = fields.String()
    price = fields.Float()


class CarQuery(Schema):
    name = fields.String()
    price = fields.Float()


class LoginData(Schema):
    username = fields.String(validate=validate.Length(min=1))
    password = fields.String()


class Token(Schema):
    access_token = fields.String()


class ListUsersReq(Schema):
    email = fields.String(validate=validate.Email())
    username = fields.String()


class UserById(Schema):
    userId = fields.Integer


class Response(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
