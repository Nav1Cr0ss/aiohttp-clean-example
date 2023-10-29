from typing import Callable

from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from internal.app.user.dto.user import UserSchema
from pkg.auth.dummy_provider.auth import DummyProvider
from pkg.server.aiohttp.errors import ErrUnauthorized


# middlewares also should be designed as a class for correct dependencies injection
# for this example I will just call dummy_provider
@middleware
async def auth(request: Request, handler: Callable) -> Response:
    dummy_provider = DummyProvider()

    try:
        user = await dummy_provider.auth_user(request.headers.get("Authorization", ""))
        request["ctx"].user = UserSchema(**user)
    except ErrUnauthorized as exc:
        return Response(text=str(exc), status=401)

    resp = await handler(request)
    return resp
