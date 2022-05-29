import bcrypt
from flask import request, Request
from src.middlewares.authentication_middleware import authenticate
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
    method_decorators = [authenticate]

    def get(self, request: Request, id: str):
        if request.current_user.id != id:
            return output_json(
                data={"error": "you are not authorized to access this data"},
                code=403,
                headers={"content-type": "application/json"},
            )

        user: User = User.objects.get(id=id)
        user.id = str(user.id)
        user_dict: dict = user.__dict__()
        return output_json(
            user_dict, code=200, headers={"content-type": "application/json"}
        )

    def put(self, request: Request, id: str):
        if request.current_user.id != id:
            return output_json(
                data={"error": "you are not authorized to access this data"},
                code=403,
                headers={"content-type": "application/json"},
            )
        data: str = request.get_json()
        user: User = User.objects.get(id=id)
        user.update(**data)
        updated_user: User = User.objects.get(id=id)
        updated_user_dict: dict = updated_user.__dict__()
        return output_json(
            updated_user_dict, code=200, headers={"content-type": "application/json"}
        )
