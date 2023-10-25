from json import JSONDecodeError

from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@middleware
async def construct_request_body(request: Request, handler: callable) -> Response:

    try:
        body = await request.json()
        request["ctx"].body = body
    except JSONDecodeError:
        return Response(text="Wrong request body", status=400)
    resp = await handler(request)
    return resp
