from aiohttp import web_exceptions as we
from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@middleware
async def upload_pdf(request: Request, handler: callable) -> Response:
    content_disposition = request.headers.get('Content-Disposition', '')
    filename = None
    if content_disposition:
        parts = content_disposition.split(';')
        for part in parts:
            if part.strip().startswith('filename='):
                filename = part.split('=')[1].strip().strip('"')

    if request.content.is_eof():
        raise we.HTTPBadRequest(
            text='Missing file in request'
        )

    if not filename:
        raise we.HTTPBadRequest(
            text='Missing filename in the request'
        )

    if request.content_type != 'application/pdf':
        raise we.HTTPUnsupportedMediaType(
            text='Invalid content type. Only PDF files are supported.',
        )

    content_length = int(request.headers['Content-Length'])
    if content_length > 104857600:
        raise we.HTTPRequestEntityTooLarge(
            max_size=104857600,
            actual_size=content_length
        )

    request["ctx"].extra["filename"] = filename
    resp = await handler(request)
    return resp
