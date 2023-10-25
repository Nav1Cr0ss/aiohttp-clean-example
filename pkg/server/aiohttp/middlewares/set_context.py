from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from pkg.server.aiohttp.data import Context


@middleware
async def set_context(request: Request, handler: callable) -> Response:
    request["ctx"] = Context({},{})
    resp = await handler(request)
    return resp
