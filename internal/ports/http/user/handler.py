import json

from aiohttp.web_request import Request
from aiohttp.web_response import Response
from pydantic import ValidationError

from internal.app.app import UserAppIface
from internal.app.user.dto.user import UserListSchema
from internal.domain.account import RoleEnum
from internal.ports.http.handler import UserHandlerIface
from internal.ports.http.user.dto.user_create import UserCreateBody
from internal.ports.http.user.dto.user_filter_params import UserParamRequest
from internal.ports.http.user.dto.user_id_param import UserIdParam
from internal.ports.http.user.dto.user_partial_update import UserPartialUpdateBody
from pkg.server.aiohttp.errors import ApiError, ErrUnauthorized


class UserHandler(UserHandlerIface):
    def __init__(self, app: UserAppIface):
        self.app = app

    permissions = {

    }

    async def get_users(self, request: Request) -> Response:
        try:
            filter_params = UserParamRequest(**request.query)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        users: UserListSchema = await self.app.get_users(filter_params)
        return Response(text=users.model_dump_json(), content_type='application/json', status=200)

    async def create_user(self, request: Request) -> Response:
        try:
            user_body = UserCreateBody(**request["ctx"].body)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        try:
            user_id: int = await self.app.create_user(user_body)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        return Response(text=json.dumps({"id": user_id}), content_type='application/json', status=200)

    async def login_user(self, request: Request) -> Response:
        try:
            user_body = UserCreateBody(**request["ctx"].body)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        try:
            jwt_token = await self.app.login_user(user_body)
        except ErrUnauthorized as ue:
            return Response(text=str(ue), content_type='application/json', status=ue.code)

        return Response(text=json.dumps({"token": jwt_token}), status=200)

    async def partial_update_user(self, request: Request) -> Response:
        # just for simplification - there is should be created permission framework
        user = request["ctx"].user
        if user.role != RoleEnum.admin:
            return Response(text="forbidden", content_type='application/json', status=403)

        try:
            user_param = UserIdParam(**request.match_info)
            user_body = UserPartialUpdateBody(**request["ctx"].body)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        try:
            await self.app.partial_update_user(user_param.id, user_body)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        return Response(content_type='application/json', status=201)
