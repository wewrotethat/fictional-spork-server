from src.controllers.image_upload_controller import ImageUploadController
from src.controllers.lab_test_entry_controller import (
    LabTestEntriesController,
    LabTestEntryController,
    TechnicialLabTestEntriesController,
)
from src.controllers.auth_controller import AuthController
from src.controllers.user_controller import UserController, UsersController


def initialize_routes(api):
    api.add_resource(UsersController, "/api/users")
    api.add_resource(UserController, "/api/users/<id>")
    api.add_resource(AuthController, "/api/auth")
    api.add_resource(
        TechnicialLabTestEntriesController,
        "/api/users/<technician_id>/lab-test-entries",
    )
    api.add_resource(LabTestEntriesController, "/api/lab-test-entries")
    api.add_resource(LabTestEntryController, "/api/lab-test-entries/<id>")
