from datetime import datetime, timedelta
from json import JSONEncoder
import os

import jwt
import bcrypt
from flask import Response, request
from flask_restful import Resource, output_json

from src.models.user import User


class AuthController(Resource):
    def post(self):
        """
        Authenticate a user using username and password
        """
        error_response = Response(JSONEncoder().encode({"success": False}), status=400)
        try:
            data: dict = request.json
            username: str = data["username"]
            password: str = data["password"]
            user: User = User.objects.get(username=username)
            byte_password: bytearray = password.encode("utf-8")
            byte_hashed_password: bytearray = user.password.encode("utf-8")
            password_matches = bcrypt.checkpw(byte_password, byte_hashed_password)
            if password_matches:
                expiry_time: datetime = datetime.utcnow() + timedelta(hours=6)

                jwt_token: str = jwt.encode(
                    {"username": username, "id": str(user.id), "exp": expiry_time},
                    os.environ["JWT_SECRET"],
                    algorithm="HS256",
                )
                return output_json(
                    code=200,
                    data={"success": True, "token": jwt_token},
                    headers={"content-type": "application/json"},
                )
            else:
                return error_response
        except Exception as e:
            return error_response
