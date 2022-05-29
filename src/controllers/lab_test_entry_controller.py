import bcrypt
from flask import request, Request
from src.middlewares.authentication_middleware import authenticate
from src.models.lab_test_entry import LabTestEntry
from flask_restful import Resource, output_json
from mongoengine.errors import ValidationError, NotUniqueError


class LabTestEntriesController(Resource):
    method_decorators = [authenticate]

    def post(self, req: Request):
        try:
            data: str = request.get_data()
            lab_test_entry: LabTestEntry = LabTestEntry.from_json(data)
            lab_test_entry.technician_id = req.current_user.id
            lab_test_entry.save()
            lab_test_entry_dict: dict = lab_test_entry.__dict__()
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
                data={"error": "some error occurred in our servers"},
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

        lab_test_entries: list = LabTestEntry.objects(technician_id=technician_id)
        lab_test_entry_dicts: list = [
            lab_test_entry.__dict__() for lab_test_entry in lab_test_entries
        ]
        return output_json(
            data=lab_test_entry_dicts,
            code=200,
            headers={"content-type": "application/json"},
        )


class LabTestEntryController(Resource):
    method_decorators = [authenticate]

    def get(self, req: Request, id: str):
        lab_test_entry: LabTestEntry = LabTestEntry.objects.get(id=id)
        lab_test_entry.id = str(lab_test_entry.id)
        lab_test_entry_dict: dict = lab_test_entry.__dict__()
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
