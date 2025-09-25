from flask_restful import Resource, request
from database import SessionLocal
import models
from datetime import date
from marshmallow import Schema, fields
from marshmallow import ValidationError


class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterUser(LoginUserSchema):
    email = fields.Email(required=True)

class CheckUser(Schema):
    username = fields.Str(required=True)


check_username = CheckUser()
login_schema = LoginUserSchema()
register_schema = RegisterUser()



class RegisterUser(Resource):
    def get(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = check_username.load(data)
        except ValidationError as error:
            return {"message": "Wrong request"}, 400

        session = SessionLocal()
        user = session.query(models.User).filter(
            models.User.username == data['username']
        ).first()
        session.close()
        if user:
            return { "username": user.username}, 200
        return {"message": "User not found"}, 200

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400

        try:
            data = register_schema.load(data)
        except ValidationError as error:
            return {"message": "Invalid request"}, 400
        new_user = models.User(**data)

        session = SessionLocal()
        user = session.query(models.User).filter(
            models.User.username == data['username']
        ).first()
        if user:
            return {"message": "User already exist"}, 409

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()
        return {"message": "Created new user"}, 201

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = login_schema.load(data)
        except ValidationError as error:
            return {"message": "Wrong request"}, 400
        session = SessionLocal()
        user = session.query(models.User).filter(
            models.User.username == data['username']
        ).first()

        if user:
            if user.password == data['password']:
                return {"message": "Logged in"}, 200
        else:
            return {"message": "User not found"}, 404