from src.db.dependencies import (get_unit_of_work, get_user_repository,
                                 get_auth_repository)
from src.services.auth.service import AuthService
from src.services.user.service import UserService


def get_auth_service():
    return AuthService(get_unit_of_work(), get_user_repository(), get_auth_repository())

def get_user_service():
    return UserService(get_unit_of_work(), get_user_repository())
