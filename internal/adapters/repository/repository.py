from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.engine import ScalarResult

from internal.adapters.repository.postgres.drawing.dto.create_file import CreateFileData
from internal.adapters.repository.postgres.user.dto.create_user import CreateUserData
from internal.adapters.repository.postgres.user.dto.partial_update_user import (
    PartialUpdateUserData,
)
from internal.app.drawing.dto.file import DrawingFilter
from internal.app.drawing.dto.file_history import DrawingHistoryFilter
from internal.app.user.dto.user import UserFilter
from internal.domain.account import User
from internal.domain.file import File, FileHistory


class DrawingRepoIface(ABC):
    @abstractmethod
    async def get_drawing(self, drawing_id: int) -> Optional[File]:
        ...

    @abstractmethod
    async def create_file_data(self, file_data: CreateFileData) -> int:
        ...

    @abstractmethod
    async def get_drawings(self, filters: DrawingFilter) -> ScalarResult[tuple[File]]:
        ...

    @abstractmethod
    async def get_drawings_history(
        self, filters: DrawingHistoryFilter
    ) -> ScalarResult[tuple[FileHistory]]:
        ...


class UserRepoIface(ABC):
    @abstractmethod
    async def get_users(self, filters: UserFilter) -> ScalarResult[tuple[User]]:
        ...

    @abstractmethod
    async def create_user(self, user_data: CreateUserData) -> int:
        ...

    @abstractmethod
    async def partial_update_user(
        self, user_id: int, update_data: PartialUpdateUserData
    ) -> None:
        ...
