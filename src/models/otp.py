from datetime import datetime
from enum import unique
from src.database.db import db


class Otp(db.Document):
    user_id = db.ObjectIdField(required=True, db_field="userId")
    phone_number = db.StringField(max_length=50, required=True, db_field="phoneNumber")
    otp = db.StringField(required=True, db_field="otp")
    verified = db.BooleanField(default=False, db_field="verified")
    created_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="createdAt"
    )
    updated_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="updatedAt"
    )

    def __dict__(self):
        return {
            "id": str(self.id),
            "userId": str(self.user_id),
            "phoneNumber": self.phone_number,
            "otp": self.otp,
            "verified": self.verified,
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
        }
