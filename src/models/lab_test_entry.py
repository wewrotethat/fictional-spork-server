from datetime import datetime
from enum import unique
from src.models.lab_result import LabResult
from src.database.db import db
from src.models.enums.phone_verification_status import PhoneVerificationStatus
from src.models.enums.profile_verification_status import ProfileVerificationStatus


class LabTestEntry(db.Document):
    technician_id = db.StringField(
        max_length=50, required=True, db_field="technicianId"
    )
    patient_id = db.StringField(max_length=50, required=True, db_field="patientId")
    blood_smear_image_url = db.StringField(db_field="bloodSmearImageUrl")
    result = db.EmbeddedDocumentField(
        LabResult,
        db_field="medicalLicenseId",
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
            "patientId": self.patient_id,
            "technicianId": self.technician_id,
            "bloodSmearImageUrl": self.blood_smear_image_url,
            "result": self.result.__dict__() if self.result else None,
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
        }
