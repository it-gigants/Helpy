from src.db.db_helper import db_helper
from src.db.repositories import AuthRepository, UserRepository
from src.db.unit_of_work import UnitOfWork


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork(db_helper.session_factory)

def get_auth_repository() -> AuthRepository:
    return AuthRepository()

def get_user_repository() -> UserRepository:
    return UserRepository()
