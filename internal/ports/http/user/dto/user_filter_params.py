from typing import Optional


from internal.app.user.dto.user import UserFilter
from internal.domain.account import RoleEnum


class UserParamRequest(UserFilter):
    role: Optional[RoleEnum] = None
    username: Optional[str] = None
