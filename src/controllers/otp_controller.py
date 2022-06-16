import bcrypt
from flask import Request
from flask_restful import output_json, Resource
from src.helpers.otp_message_builder import OtpMessageBuilder
from src.services.sms_service import SmsService
from src.helpers.otp_generator import generateOtp
from src.models.otp import Otp
from src.models.enums.phone_verification_status import PhoneVerificationStatus

from src.models.user import User
from src.middlewares.authentication_middleware import authenticate


class OtpController(Resource):
    method_decorators = [authenticate]

    def get(self, req: Request):
        current_user: User = req.current_user
        if current_user.phone_verification_status == PhoneVerificationStatus.VERIFIED:
            return output_json(
                data={"error": "phone number already verified"},
                code=400,
                headers={"content-type": "application/json"},
            )
        try:
            otp_code = generateOtp()
            byte_password: bytearray = otp_code.encode("utf-8")
            salt: str = bcrypt.gensalt()
            hashed_password: str = bcrypt.hashpw(byte_password, salt)
            otp: Otp = Otp(
                user_id=current_user.id,
                phone_number=current_user.phone_number,
                otp=hashed_password.decode("utf8"),
            )
            otp.save()
            sms_result = SmsService().send_sms(
                otp.phone_number, OtpMessageBuilder.build(otp_code)
            )

            if sms_result:
                return output_json(
                    data={
                        "message": f"OTP has been sent to {current_user.phone_number}"
                    },
                    code=200,
                    headers={"content-type": "application/json"},
                )
            else:
                return output_json(
                    data={"error": "error sending sms"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

        except Exception as e:
            return output_json(
                data={"error": "some error occurred in our db"},
                code=500,
                headers={"content-type": "application/json"},
            )
