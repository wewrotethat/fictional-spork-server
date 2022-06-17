from flask import Request, request
from flask_restful import Resource, output_json
from src.services.cloud_messaging import sendPushForTokens
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
            user: User = User.objects.get(id=user_id)
            user.profile_verification_status = ProfileVerificationStatus[
                verification_status.upper()
            ]
            user.save()
            sendPushForTokens(self.getTitle(user), self.getBody(user), user.device_tokens, {
                'event': 'ACCOUNT_APPROVAL',
                'user_id': str(user.id)
            })
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

    def getTitle(_: User):
        return f"Profile Verification Status Update"

    def getBody(user: User):
        if user.profile_verification_status == ProfileVerificationStatus.REJECTED:
            return f"Dear {user.first_name}, your request to verify your account has been Rejected. Please resubmit a correct Medical License ID."
        elif user.profile_verification_status == ProfileVerificationStatus.VERIFIED:
            return f"Dear {user.first_name}, your account has been verified. You can continue to use the app."

        return "Sorry to disturb you your peace. Someone in our team will be punished for this."
