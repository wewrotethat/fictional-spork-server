from json import JSONEncoder
from flask import request, Response
from src.models.user import User
from flask_restful import Resource
from mongoengine.errors import ValidationError


class UsersController(Resource):
    def post(self):
        try:
            data: str = request.get_data()
            user: User = User.from_json(data)
            user.save()
            user_dict: dict = user.__dict__()
            user_json: str = JSONEncoder().encode(user_dict)
            return Response(user_json, mimetype="application/json", status=201)
        except ValidationError as e:
            return Response(JSONEncoder().encode({"error": e.message}), status=400)
        except Exception as e:
            return Response(JSONEncoder().encode({"error": e}), status=500)

class UserController(Resource):
    def get(self, id: str):
        user: User = User.objects.get(id=id)
        user.id = str(user.id) 
        user_dict: dict = user.__dict__()
        user_json: str = JSONEncoder().encode(user_dict)
        return Response(user_json, mimetype="application/json", status=200)

    def put(self, id: str):
        data: str = request.get_json()
        user: User = User.objects.get(id=id)
        user.update(**data)
        updated_user: User = User.objects.get(id=id)
        updated_user_dict: dict = updated_user.__dict__()
        updated_user_json: str = JSONEncoder().encode(updated_user_dict)
        return Response(updated_user_json, mimetype="application/json", status=200)
