from pydantic import BaseModel, EmailStr, field_validator, Field
import re


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Validation of first name and last name."""
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty or contain only spaces")
        if not re.match(r"^[а-яА-ЯёЁa-zA-Z\s\-]+$", value):
            raise ValueError("Name can only contain letters, spaces and hyphens")
        return value.title()
