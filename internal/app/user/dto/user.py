from typing import Optional

from pydantic import RootModel, BaseModel, Field

from internal.domain.account import User, RoleEnum
from pkg.pydantic_sqlalchemy.connector import sqlalchemy_to_pydantic

# Just for time saving. I don't recommend to use this in production. At least in this way
PydanticUser = sqlalchemy_to_pydantic(User)


class UserSchema(PydanticUser):
    password_hash: Optional[str] = Field(
        exclude=True,
        default=None

    )

    class Config:
        from_attributes = True


class UserListSchema(RootModel):
    root: list[UserSchema]


class UserFilter(BaseModel):
    role: Optional[RoleEnum] = None
    username: Optional[str] = None
