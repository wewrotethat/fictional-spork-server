from src.controllers.user_approval_controller import UserApprovalController
from src.controllers.otp_controller import OtpController
from src.controllers.lab_test_entry_controller import (
    LabTestEntriesController,
    LabTestEntryController,
    LabTestEntrySampleImageController,
    TechnicialLabTestEntriesController,
)
from src.controllers.auth_controller import AuthController
from src.controllers.user_controller import (
    UserController,
    UserProfilePictureController,
    UsersController,
)


def initialize_routes(api):
    api.add_resource(AuthController, "/api/auth")
    api.add_resource(UsersController, "/api/users")
    api.add_resource(UserController, "/api/users/me")
    api.add_resource(OtpController, "/api/users/otp")
    api.add_resource(UserProfilePictureController, "/api/users/profile-picture")
    api.add_resource(
        TechnicialLabTestEntriesController,
        "/api/users/me/lab-test-entries",
    )
    api.add_resource(
        LabTestEntrySampleImageController, "/api/lab-test-entries/<id>/sample-image"
    )
    api.add_resource(LabTestEntriesController, "/api/lab-test-entries")
    api.add_resource(LabTestEntryController, "/api/lab-test-entries/<id>")

    # admin endpoints
    api.add_resource(UserApprovalController, "/api/admin/users/approval")
