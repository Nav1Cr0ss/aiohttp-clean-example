from typing import Optional

from internal.adapters.repository.postgres.user.dto.create_user import CreateUserData
from internal.adapters.repository.postgres.user.dto.partial_update_user import (
    PartialUpdateUserData,
)
from internal.adapters.repository.repository import UserRepoIface
from internal.app.app import UserAppIface
from internal.app.user.dto.user import UserFilter, UserListSchema, UserSchema
from internal.ports.http.user.dto.user_create import UserCreateBody
from internal.ports.http.user.dto.user_partial_update import UserPartialUpdateBody
from pkg.auth.provider import AuthProviderIface
from pkg.server.aiohttp.errors import ErrAlreadyExist, ErrNotFount, ErrUnauthorized


class UserApp(UserAppIface):
    def __init__(self, repo: UserRepoIface, auth: AuthProviderIface):
        self.repo = repo
        self.auth = auth

    async def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        # There is better to create more simple exist sql method
        users = await self.repo.get_users(UserFilter(username=username))
        return UserSchema.model_validate(users.one_or_none())

    async def get_users(self, filters: UserFilter) -> UserListSchema:
        users = await self.repo.get_users(filters)
        return UserListSchema([UserSchema.model_validate(user) for user in users])

    async def create_user(self, user_payload: UserCreateBody) -> int:
        if await self.get_user_by_username(username=user_payload.username):
            raise ErrAlreadyExist("User with this username already exists")

        # More real example. there is I cast App layer Entity into Rep layer entity
        user_id = await self.repo.create_user(
            CreateUserData(
                username=user_payload.username,
                password_hash=await self.auth.hash_password(user_payload.password),
            )
        )

        return user_id

    async def login_user(self, user_payload: UserCreateBody) -> str:
        user = await self.get_user_by_username(username=user_payload.username)
        if not user:
            raise ErrNotFount("User with this username already exists")

        entered_password = await self.auth.hash_password(user_payload.password)

        if entered_password != user.password_hash:
            raise ErrUnauthorized("Username or password are incorrect")

        token = await self.auth.get_credentials(UserSchema.model_validate(user))
        return token

    async def partial_update_user(
        self, user_id: int, user_payload: UserPartialUpdateBody
    ) -> None:
        await self.repo.partial_update_user(
            user_id=user_id,
            update_data=PartialUpdateUserData(
                role=user_payload.role,
            ),
        )
