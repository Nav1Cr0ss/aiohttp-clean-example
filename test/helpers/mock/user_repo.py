from internal.adapters.repository.postgres.user.dto.create_user import CreateUserData
from internal.adapters.repository.postgres.user.dto.partial_update_user import (
    PartialUpdateUserData,
)
from internal.adapters.repository.repository import UserRepoIface
from internal.app.user.dto.user import UserFilter
from internal.domain.account import User
from test.helpers.mock.scallar_result import MockScalarResult


# TODO: create possibility to setup return values


class UserRepoMock(UserRepoIface):
    async def get_users(self, filters: UserFilter) -> MockScalarResult[tuple[User | None]]:
        return MockScalarResult((None,))

    async def create_user(self, user_data: CreateUserData) -> int:
        return 123

    async def partial_update_user(
            self, user_id: int, update_data: PartialUpdateUserData
    ) -> None:
        ...
