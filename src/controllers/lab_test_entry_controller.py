import os
import bcrypt
import requests
import werkzeug
from flask import request, Request
from src.services.hospital_service import getPatientInfo
from src.middlewares.authentication_middleware import authenticate
from src.models.lab_test_entry import LabTestEntry
from flask_restful import Resource, output_json, reqparse
from mongoengine.errors import ValidationError, NotUniqueError

from src.services.image_upload import (
    upload_image_to_cloud_storage,
    upload_image_service,
)


class LabTestEntriesController(Resource):
    method_decorators = [authenticate]

    def post(self, req: Request):
        try:
            data: str = request.get_data()
            data_dict: dict = request.get_json()
            if "patientId" not in data_dict:
                return output_json(
                    data={"message": "patientId is missing"},
                    code=400,
                    headers={"content-type": "application/json"},
                )
            patient_id = data_dict["patientId"]
            patient_info = getPatientInfo(patientId=patient_id)

            lab_test_entry: LabTestEntry = LabTestEntry.from_json(data)
            lab_test_entry.technician_id = req.current_user.id

            lab_test_entry.save()
            lab_test_entry_dict: dict = lab_test_entry.__dict__()
            lab_test_entry_dict['patientInfo'] = patient_info
            return output_json(
                data=lab_test_entry_dict,
                code=201,
                headers={"content-type": "application/json"},
            )
        except ValidationError as e:
            return output_json(
                data={"error": str(e)},
                code=400,
                headers={"content-type": "application/json"},
            )
        except NotUniqueError as e:
            return output_json(
                data={"error": str(e)},
                code=400,
                headers={"content-type": "application/json"},
            )
        except Exception as e:
            return output_json(
                data={"error": str(e)},
                code=500,
            )



class TechnicialLabTestEntriesController(Resource):
    method_decorators = [authenticate]

    def get(self, req: Request, technician_id: str):
        if req.current_user.id != technician_id:
            return output_json(
                data={"error": "you are not authorized to access this data"},
                code=403,
                headers={"content-type": "application/json"},
            )
        
        lab_test_entries_dict: list = []

        lab_test_entries: list = LabTestEntry.objects(technician_id=technician_id)
        for lab_test_entry in lab_test_entries:
            lab_test_entry_dict: dict = lab_test_entry.__dict__()
            patient_info = getPatientInfo(patientId=lab_test_entry.patient_id)
            lab_test_entry_dict['patientInfo'] = patient_info
            lab_test_entries_dict.append(lab_test_entry_dict)
        return output_json(
            data=lab_test_entries_dict,
            code=200,
            headers={"content-type": "application/json"},
        )


class LabTestEntryController(Resource):
    method_decorators = [authenticate]

    def get(self, req: Request, id: str):
        lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        patient_info = getPatientInfo(patientId=lab_test_entry.patient_id)
        lab_test_entry.id = str(lab_test_entry.id)
        lab_test_entry_dict: dict = lab_test_entry.__dict__()
        lab_test_entry_dict['patientInfo'] = patient_info
        return output_json(
            lab_test_entry_dict, code=200, headers={"content-type": "application/json"}
        )

    def put(self, req: Request, id: str):
        data: str = request.get_json()
        lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        if req.current_user.id != lab_test_entry.technician_id:
            return output_json(
                data={"error": "you are not authorized to modify this data"},
                code=403,
                headers={"content-type": "application/json"},
            )

        lab_test_entry.update(**data)
        updated_lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        updated_lab_test_entry_dict: dict = updated_lab_test_entry.__dict__()
        return output_json(
            updated_lab_test_entry_dict,
            code=200,
            headers={"content-type": "application/json"},
        )


class LabTestEntrySampleImageController(Resource):
    method_decorators = [authenticate]

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def put(self, req: Request, id: str):
        lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        if req.current_user.id != lab_test_entry.technician_id:
            return output_json(
                data={"error": "you are not authorized to modify this data"},
                code=403,
                headers={"content-type": "application/json"},
            )
        upload_service_res: str = upload_image_service(self.parser, id)

        if not upload_service_res:
            return output_json(
                data={"error": "image upload failed"},
                code=400,
                headers={"content-type": "application/json"},
            )

        lab_test_entry.update(set__blood_smear_image_url=upload_service_res)
        updated_lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        updated_lab_test_entry_dict: dict = updated_lab_test_entry.__dict__()
        return output_json(
            updated_lab_test_entry_dict,
            code=200,
            headers={"content-type": "application/json"},
        )
