from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from src.db.models.mixins import Role


class UserDTO(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    role: Role
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class SUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class SUserCreate(SUser):
    password: str
