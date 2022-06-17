from functools import wraps
import os
import jwt
from flask import request, Request
from flask_restful import output_json

from src.models.user import User


def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user: User = request.current_user
        if not current_user:
            return output_json(
                data={"message": "logged in user is missing"},
                code=401,
                headers={"content-type": "application/json"},
            )
        if "admin" not in current_user.roles:
            return output_json(
                data={"message": "user is not an admin"},
                code=401,
                headers={"content-type": "application/json"},
            )
        return f(request, *args, **kwargs)

    return decorator
