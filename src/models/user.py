from datetime import datetime
from enum import unique
from src.database.db import db
from src.models.enums.phone_verification_status import PhoneVerificationStatus
from src.models.enums.profile_verification_status import ProfileVerificationStatus


class User(db.Document):
    # id = db.ObjectIdField(primary_key=True, db_field='_id')
    first_name = db.StringField(max_length=50, required=True, db_field="firstName")
    last_name = db.StringField(max_length=50, required=True, db_field="lastName")
    medical_license_id = db.StringField(
        max_length=50, required=True, unique=True, db_field="medicalLicenseId"
    )
    username = db.StringField(max_length=50, required=True, unique=True)
    password = db.StringField(required=True)
    phone_number = db.StringField(
        max_length=50, required=True, unique=True, db_field="phoneNumber"
    )
    profile_verification_status = db.EnumField(
        ProfileVerificationStatus,
        default=ProfileVerificationStatus.UNVERIFIED,
        db_field="profileVerificationStatus",
    )
    profile_picture = db.StringField(
        max_length=50, required=True, db_field="profilePicture"
    )
    phone_verification_status = db.EnumField(
        PhoneVerificationStatus,
        default=PhoneVerificationStatus.UNVERIFIED,
        db_field="phoneVerificationStatus",
    )
    # TODO: check this
    device_tokens = db.ListField(
        db.StringField(max_length=50), default=[], db_field="deviceTokens"
    )
    created_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="createdAt"
    )
    updated_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="updatedAt"
    )

    def __dict__(self):
        return {
            "id": str(self.id),
            "firstName": self.first_name,
            "lastName": self.last_name,
            "medicalLicenseId": self.medical_license_id,
            "username": self.username,
            "phoneNumber": self.phone_number,
            "profileVerificationStatus": self.profile_verification_status,
            "profilePicture": self.profile_picture,
            "phoneVerificationStatus": self.phone_verification_status,
            "deviceTokens": self.device_tokens,
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
        }
