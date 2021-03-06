from datetime import datetime, timedelta
from json import JSONEncoder
import os

import jwt
import bcrypt
from flask import Request, Response, request
from flask_restful import Resource, output_json
from src.middlewares.authentication_middleware import authenticate

from src.models.user import User


class AuthController(Resource):
    def post(self):
        """
        Authenticate a user using username and password
        """
        error_response = Response(JSONEncoder().encode({"success": False}), status=400)
        try:
            data: dict = request.json
            email: str = data["email"]
            password: str = data["password"]
            device_token: str = data["deviceToken"] if "deviceToken" in data else None
            user: User = User.objects.get(email=email)
            byte_password: bytearray = password.encode("utf-8")
            byte_hashed_password: bytearray = user.password.encode("utf-8")
            password_matches = bcrypt.checkpw(byte_password, byte_hashed_password)
            if password_matches:
                expiry_time: datetime = datetime.utcnow() + timedelta(hours=6)
                if device_token and not device_token.isspace and len(device_token) > 0:
                    existing_device_tokens: list = user.device_tokens
                    device_token_set = set(
                        existing_device_tokens if existing_device_tokens else []
                    )
                    device_token_set.add(device_token)

                    user.device_tokens = list(device_token_set)
                    user.save()

                jwt_token: str = jwt.encode(
                    {"id": str(user.id), "exp": expiry_time},
                    os.environ["JWT_SECRET"],
                    algorithm="HS256",
                )
                return output_json(
                    code=200,
                    data={
                        "id": str(user.id),
                        "success": True,
                        "token": jwt_token,
                    },
                    headers={"content-type": "application/json"},
                )
            else:
                return error_response
        except Exception as _:
            return error_response

    @authenticate
    def delete(req: Request, _):
        try:
            device_token: str = req.args["deviceToken"] if "deviceToken" else None
            if device_token:
                current_user = req.current_user
                if device_token in current_user.device_tokens:

                    current_user.device_tokens.remove(device_token)
                    current_user.save()
            return output_json(
                data={'message': "user has been logged out"},
                code=200,
                headers={"content-type": "application/json"},
            )
        except Exception as _:
            return output_json(
                data={"error": "some error occurred in our servers"},
                code=500,
                headers={"content-type": "application/json"},
            )
