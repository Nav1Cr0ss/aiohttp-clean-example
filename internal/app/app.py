from abc import ABC, abstractmethod
from typing import Optional

from aiohttp import StreamReader, BodyPartReader

from internal.app.drawing.dto.file import DrawingFilter, FileListSchema
from internal.app.drawing.dto.file_history import (
    DrawingHistoryFilter,
    FileHistoryListSchema,
)
from internal.app.user.dto.user import UserListSchema, UserFilter, UserSchema
from internal.ports.http.user.dto.user_create import UserCreateBody
from internal.ports.http.user.dto.user_partial_update import UserPartialUpdateBody


class DrawingAppIface(ABC):
    @abstractmethod
    async def get_drawings(self, filters: DrawingFilter) -> FileListSchema:
        ...

    @abstractmethod
    async def get_drawings_history(
        self, filters: DrawingHistoryFilter
    ) -> FileHistoryListSchema:
        ...

    @abstractmethod
    async def get_drawing_history(self, drawing_id: int) -> FileHistoryListSchema:
        ...

    @abstractmethod
    async def upload_drawing(
        self,
        file_stream: StreamReader | BodyPartReader,
        content_type: str,
        file_name: str,
        user_id: int,
    ) -> Optional[int]:
        ...


class UserAppIface(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        ...

    @abstractmethod
    async def get_users(self, filters: UserFilter) -> UserListSchema:
        ...

    @abstractmethod
    async def create_user(self, user_payload: UserCreateBody) -> int:
        ...

    @abstractmethod
    async def login_user(self, user_payload: UserCreateBody) -> str:
        ...

    @abstractmethod
    async def partial_update_user(
        self, user_id: int, user_payload: UserPartialUpdateBody
    ) -> None:
        ...
