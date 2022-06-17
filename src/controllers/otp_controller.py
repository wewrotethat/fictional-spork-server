from datetime import timedelta, datetime
import bcrypt
from flask import Request, request
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
            byte_otp: bytearray = otp_code.encode("utf-8")
            salt: str = bcrypt.gensalt()
            hashed_password: str = bcrypt.hashpw(byte_otp, salt)
            Otp.objects(user_id=current_user.id).delete()
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
                data={"error": "some error occurred in our system"},
                code=500,
                headers={"content-type": "application/json"},
            )

    def post(self, req: Request):
        try:
            current_user: User = req.current_user
            data: str = request.get_json()

            otp_code: str = data["otp"]
            otp: Otp = Otp.objects.get(user_id=req.current_user.id)
            if otp is None:
                return output_json(
                    data={"error": "OTP not found"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

            if (otp.created_at + timedelta(hours=1)) < datetime.utcnow():
                return output_json(
                    data={"error": "OTP expired"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

            if otp.trials >= 3:
                return output_json(
                    data={"error": "OTP trials exceeded"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

            byte_otp: bytearray = otp_code.encode("utf-8")
            byte_hashed_otp: bytearray = otp.otp.encode("utf-8")
            otp_matches = bcrypt.checkpw(byte_otp, byte_hashed_otp)

            if otp_matches:
                current_user.phone_verification_status = (
                    PhoneVerificationStatus.VERIFIED
                )
                current_user.save()
                return output_json(
                    data={"message": "phone number verified"},
                    code=200,
                    headers={"content-type": "application/json"},
                )

            else:
                otp.trials += 1
                otp.save()
                return output_json(
                    data={"error": "OTP is incorrect"},
                    code=400,
                    headers={"content-type": "application/json"},
                )

        except Exception as e:
            return output_json(
                data={"error": "some error occurred in our system"},
                code=500,
                headers={"content-type": "application/json"},
            )
