from sqlalchemy import select, insert, update
from sqlalchemy.engine import ScalarResult

from internal.adapters.repository.postgres.user.dto.create_user import CreateUserData
from internal.adapters.repository.postgres.user.dto.partial_update_user import (
    PartialUpdateUserData,
)
from internal.adapters.repository.repository import UserRepoIface
from internal.app.user.dto.user import UserFilter
from internal.domain.account import User
from pkg.db.postgres.postgres import Postgres


class UserRepo(UserRepoIface):
    def __init__(self, db: Postgres):
        self.db = db

    async def get_users(self, filters: UserFilter) -> ScalarResult[tuple[User]]:
        stmt = select(User)
        if filters.role is not None:
            stmt = stmt.where(User.role == str(filters.role))

        if filters.username is not None:
            stmt = stmt.where(User.username == filters.username)
        users = await self.db.select(stmt)
        return users

    async def create_user(self, user_data: CreateUserData) -> int:
        stmt = insert(User).values(
            username=user_data.username,
            password_hash=user_data.password_hash,
            role=user_data.role,
        )
        user_id = await self.db.insert(stmt)
        return user_id

    async def partial_update_user(
        self, user_id: int, update_data: PartialUpdateUserData
    ) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data.as_update_data())
        )
        await self.db.update(stmt)
