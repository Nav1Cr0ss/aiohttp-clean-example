from dataclasses import dataclass
from typing import Callable, Optional, Coroutine, Any

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from internal.app.user.dto.user import UserSchema

Method = Callable[..., web.RouteDef]
Middleware = Callable[..., Coroutine[Any, Any, Response]]


@dataclass
class Route:
    url: str
    method: Method
    handler: callable
    no_auth: Optional[bool] = False
    no_cors: Optional[bool] = False
    middlewares: Optional[tuple[Middleware]] = ()


@dataclass
class Context:
    body: dict[str, Any]
    extra: dict[str, Any]
    user: Optional[UserSchema] = None


class RequestWCtx(Request):
    ctx = Context
