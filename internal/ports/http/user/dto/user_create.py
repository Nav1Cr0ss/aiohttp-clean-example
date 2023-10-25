from pydantic import BaseModel, field_validator


# Base validation, better to create validation framework
class UserCreateBody(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if len(value) < 4:
            raise ValueError("username must be at least 4 characters long")
        if not value.isalnum():
            raise ValueError("username should only contain alphanumeric characters")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("password must be at least 6 characters long")
        return value
