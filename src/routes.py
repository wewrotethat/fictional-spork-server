from src.controllers.auth_controller import AuthController
from src.controllers.user_controller import UserController, UsersController


def initialize_routes(api):
    api.add_resource(UsersController, '/api/users')
    api.add_resource(UserController, '/api/users/<id>')
    api.add_resource(AuthController, '/api/auth')