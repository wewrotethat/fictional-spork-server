import os
import requests


def getPatientInfo(patientId: str):
    try:
        url = os.environ.get('HOSPITAL_API_URL')
        response: requests.Response = requests.get(
            f"{url}/patients/{patientId}",
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        raise e
