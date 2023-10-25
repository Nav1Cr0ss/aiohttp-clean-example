from typing import Optional

from pydantic import BaseModel

from internal.domain.account import RoleEnum


class UserPartialUpdateBody(BaseModel):
    role: Optional[RoleEnum] = None
