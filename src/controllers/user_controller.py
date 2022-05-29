import bcrypt
from json import JSONEncoder
from black import out
from flask import request, Response
from src.models.user import User
from flask_restful import Resource, output_json
from mongoengine.errors import ValidationError, NotUniqueError


class UsersController(Resource):
    def post(self):
        try:
            data: str = request.get_data()
            user: User = User.from_json(data)
            byte_password: bytearray = user.password.encode("utf-8")
            salt: str = bcrypt.gensalt()
            hashed_password: str = bcrypt.hashpw(byte_password, salt)
            user.password = hashed_password.decode("utf8")
            user.save()
            user_dict: dict = user.__dict__()
            return output_json(
                data=user_dict, code=201, headers={"content-type": "application/json"}
            )
        except ValidationError as e:
            return output_json(
                data={"error": str(e)},
                code=400,
                headers={"content-type": "application/json"},
            )
        except NotUniqueError as e:
            return output_json(
                data={"error": str(e)},
                code=400,
                headers={"content-type": "application/json"},
            )
        except Exception as e:
            return output_json(
                data={"error": "some error occurred in our servers"},
                code=500,
            )


class UserController(Resource):
    def get(self, id: str):
        user: User = User.objects.get(id=id)
        user.id = str(user.id)
        user_dict: dict = user.__dict__()
        return output_json(
            user_dict, code=200, headers={"content-type": "application/json"}
        )

    def put(self, id: str):
        data: str = request.get_json()
        user: User = User.objects.get(id=id)
        user.update(**data)
        updated_user: User = User.objects.get(id=id)
        updated_user_dict: dict = updated_user.__dict__()
        return output_json(
            updated_user_dict, code=200, headers={"content-type": "application/json"}
        )
