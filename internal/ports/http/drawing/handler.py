import json

from aiohttp.web_request import Request
from aiohttp.web_response import Response
from pydantic import ValidationError

from internal.app.app import DrawingAppIface
from internal.app.drawing.dto.file import FileListSchema
from internal.app.drawing.dto.file_history import FileHistoryListSchema
from internal.ports.http.drawing.dto.drawing_filter_param import DrawingFilterParam
from internal.ports.http.drawing.dto.drawing_history_filter_param import DrawingHistoryFilterParam
from internal.ports.http.drawing.dto.drawing_id_param import DrawingIdParam
from internal.ports.http.handler import DrawingHandlerIface
from pkg.server.aiohttp.errors import ApiError


class DrawingHandler(DrawingHandlerIface):
    def __init__(self, app: DrawingAppIface):
        self.app = app

    async def get_drawings(self, request: Request) -> Response:
        try:
            filter_params = DrawingFilterParam(**request.query)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        drawings: FileListSchema = await self.app.get_drawings(filter_params)
        return Response(text=drawings.model_dump_json(), content_type='application/json', status=200)

    async def get_drawings_history(self, request: Request) -> Response:
        try:
            filter_params = DrawingHistoryFilterParam(**request.query)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        drawings_history: FileHistoryListSchema = await self.app.get_drawings_history(filter_params)
        return Response(text=drawings_history.model_dump_json(), content_type='application/json', status=200)

    async def get_drawing_history(self, request: Request) -> Response:
        try:
            drawing_history_param = DrawingIdParam(**request.match_info)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        try:
            drawing_history = await self.app.get_drawing_history(drawing_history_param.id)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        return Response(text=drawing_history.model_dump_json(), content_type='application/json', status=200)

    async def upload_drawing(self, request: Request) -> Response:
        file_stream = request.content

        # validations placed in middleware

        content_type: str = request.content_type

        # In real app we will create two name in database, original and calculated(hash or just concatenations)
        filename: str = request["ctx"].extra["filename"]

        user = request["ctx"].user
        file_id = await self.app.upload_drawing(file_stream, content_type, filename, user.id)

        return Response(text=json.dumps({"file_id": file_id}), content_type='application/json', status=200)

    async def upload_drawings(self, request: Request) -> Response:
        user = request["ctx"].user
        file_ids = []
        async for file in await request.multipart():
            file_id = await self.app.upload_drawing(file, file.headers.get("Content-Type"), file.filename, user.id)
            file_ids.append(file_id)
        return Response(text=json.dumps({"file_ids": file_ids}), content_type='application/json', status=200)
