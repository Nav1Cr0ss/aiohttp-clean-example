from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@middleware
async def cors(request: Request, handler: callable) -> Response:
    print("CORS Checked")
    resp = await handler(request)
    return resp
