from abc import ABC, abstractmethod

from aiohttp.web_request import Request
from aiohttp.web_response import Response


class DrawingHandlerIface(ABC):
    @abstractmethod
    async def upload_drawing(self, request: Request) -> Response: ...

    @abstractmethod
    async def get_drawings_history(self, request: Request) -> Response: ...

    @abstractmethod
    async def get_drawing_history(self, request: Request) -> Response: ...
    @abstractmethod
    async def get_drawings(self, request: Request) -> Response: ...


class UserHandlerIface(ABC):
    @abstractmethod
    async def get_users(self, request: Request) -> Response: ...

    @abstractmethod
    async def create_user(self, request: Request) -> Response: ...

    @abstractmethod
    async def login_user(self, request: Request) -> Response: ...

    @abstractmethod
    async def partial_update_user(self, request: Request) -> Response: ...
