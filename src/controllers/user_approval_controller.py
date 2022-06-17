from flask import Request, request
from flask_restful import Resource, output_json
from src.models.enums.profile_verification_status import ProfileVerificationStatus
from src.middlewares.authentication_middleware import authenticate
from src.middlewares.authorization_middleware import authorize

from src.models.user import User


class UserApprovalController(Resource):

    method_decorators = [authorize, authenticate]

    # third argument is ->
    def post(self, req: Request, _):
        try:
            data: str = req.get_json()
            user_id = data["userId"]
            verification_status = data["verificationStatus"]
            user = User.objects.get(id=user_id)
            user.profile_verification_status = ProfileVerificationStatus[
                verification_status.upper()
            ]
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
