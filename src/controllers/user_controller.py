import bcrypt
from flask import request, Request
from src.helpers.validators.user_validators.user_validators import UserValidators
from src.services.image_upload import upload_image_service
from src.middlewares.authentication_middleware import authenticate
from src.models.user import User
from flask_restful import Resource, output_json, reqparse
from mongoengine.errors import ValidationError, NotUniqueError, FieldDoesNotExist


class UsersController(Resource):
    @authenticate
    # args had to be flipped because of argument unpacking in the authenticate middleware
    def get(req: Request, _):
        try:
            user: User = User.objects.get(id=req.current_user.id)
            user_dict: dict = user.__dict__()
            return output_json(
                data=user_dict, code=200, headers={"content-type": "application/json"}
            )
        except FieldDoesNotExist as e:
            return output_json(
                data={"error": str(e)},
                code=400,
                headers={"content-type": "application/json"},
            )
        except Exception as e:
            return output_json(
                data={"error": "some error occurred in our servers"},
                code=500,
                headers={"content-type": "application/json"},
            )

    def post(self):
        try:
            data_dict: dict = request.get_json()
            validation_result: list = UserValidators().validateSignUpInput(data_dict)
            if len(validation_result) > 0:
                return output_json(
                    data={"validation_errors": validation_result},
                    code=400,
                    headers={"content-type": "application/json"},
                )
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
        except Exception as e:
            return output_json(
                data={"error": "some error occurred in our servers"},
                code=500,
                headers={"content-type": "application/json"},
            )

    @authenticate
    # args had to be flipped because of argument unpacking in the authenticate middleware
    def put(req: Request, _):
        id = req.current_user.id
        data: str = request.get_json()
        user: User = User.objects.get(id=id)
        user.update(**data)
        updated_user: User = User.objects.get(id=id)
        updated_user_dict: dict = updated_user.__dict__()
        return output_json(
            updated_user_dict, code=200, headers={"content-type": "application/json"}
        )


class UserController(Resource):
    method_decorators = [authenticate]

    def get(self, req: Request, id: str):
        user: User = User.objects.get(id=id)
        user.id = str(user.id)
        user_dict: dict = user.__dict__()
        return output_json(
            user_dict, code=200, headers={"content-type": "application/json"}
        )

    def put(self, req: Request, id: str):
        if req.current_user.id != id:
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


class UserProfilePictureController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    method_decorators = [authenticate]

    def put(self, req: Request):
        try:
            user: User = req.current_user
            image_url: str = upload_image_service(self.parser, user.id)

            if not image_url:
                return output_json(
                    data={"error": "image upload failed"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

            user.profile_picture_url = image_url
            return output_json(
                user.__dict__(),
                code=200,
                headers={"content-type": "application/json"},
            )

        except Exception as _:
            return output_json(
                data={"error": "some error occurred in our servers"},
                code=500,
                headers={"content-type": "application/json"},
            )
