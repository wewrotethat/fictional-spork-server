from src.services.cloud_messaging import sendPushForTokens
from src.models.user import User
from src.models.lab_result import LabResult
from src.models.lab_test_entry import LabTestEntry


"""
1, young trophozoites (ring forms); 2, growing trophozoites; 3, mature trophozoites; 4, mature schizonts; 5, macrogametocytes; 6, microgametocytes.
"""


def run_recognition_model():
    print("running model")
    try:
        entries = LabTestEntry.objects(status="queued")
        for entry in entries:
            try:
                entry.result = LabResult(status="infected", stage="1")
                entry.status = "ready"
                entry.save()
                owner: User = User.objects.get(id=entry.technician_id)
                sendPushForTokens(owner.device_tokens)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
