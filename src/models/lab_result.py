from datetime import datetime
from enum import unique
from src.database.db import db
from src.models.enums.phone_verification_status import PhoneVerificationStatus
from src.models.enums.profile_verification_status import ProfileVerificationStatus


class LabResult(db.EmbeddedDocument):
    status = db.StringField(max_length=50, required=True, db_field="status")
    stage = db.StringField(max_length=50, required=True, db_field="stage")
    segmented_image_url = db.StringField(required=True, db_field="segmentedImageUrl")
    extra = db.DictField(max_length=50, required=True, db_field="extra")
    created_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="createdAt"
    )
    updated_at = db.DateTimeField(
        required=True, default=datetime.utcnow, db_field="updatedAt"
    )

    def __dict__(self):
        return {
            "status": self.status,
            "stage": self.stage,
            "segmentedImageUrl": self.segmented_image_url,
            "extra": self.extra,
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
        }
