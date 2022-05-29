from functools import wraps
import os
import jwt
from flask import request, Request
from flask_restful import output_json

from src.models.user import User


def authenticate(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        authorization_header = None

        if 'Authorization' in request.headers:
            authorization_header = request.headers['Authorization']

        if not authorization_header:
            return output_json(data={'message': 'authorization header is missing'}, code=401, headers={'content-type': 'application/json'})
        if not authorization_header.startswith('Bearer '):
            return output_json(data={'message': 'authorization header should have a Bearer token'}, code=401, headers={'content-type': 'application/json'})
        token = authorization_header.replace('Bearer ', '')

        try:
            data = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=["HS256"])
            current_user = User.objects.get(id=data['id'])
            current_user.id = str(current_user.id)
        except Exception as e:
            return output_json(data={'message': 'token is invalid'}, code=401, headers={'content-type': 'application/json'})

        return f(current_user, *args, **kwargs)
    return decorator