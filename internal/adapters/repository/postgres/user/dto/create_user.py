from dataclasses import dataclass
from typing import Optional

from internal.domain.account import RoleEnum


@dataclass
class CreateUserData:
    username: str
    password_hash: str
    role: Optional[RoleEnum] = RoleEnum.staff
