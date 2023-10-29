from abc import ABC, abstractmethod
from typing import Optional

from internal.app.user.dto.user import UserSchema


class AuthProviderIface(ABC):
    # There is should method for auth, invoce etc. methods

    @abstractmethod
    async def hash_password(self, raw_password: str) -> str:
        ...

    @abstractmethod
    async def auth_user(self, token: str) -> Optional[dict]:
        ...

    @abstractmethod
    async def get_credentials(self, user: UserSchema) -> str:
        ...
