from dataclasses import dataclass
from typing import Optional

from internal.domain.account import RoleEnum
from pkg.orm.data import PartialUpdate


@dataclass
class PartialUpdateUserData(PartialUpdate):
    role: Optional[RoleEnum] = RoleEnum.staff
