import pytest

from internal.app.user.app import UserApp
from internal.ports.http.user.dto.user_create import UserCreateBody
from pkg.auth.dummy_provider.auth import DummyProvider
from test.helpers.mock.user_repo import UserRepoMock


# Just example how it should work
# The idea was to create easy-testable architecture without Monkey Patching
# For testing App layer we have to create mocks for repo and storage
# On current solution db and storage don't have interfaces
# storage="Background" - just placeholder to make it work


@pytest.mark.asyncio
async def test_create_user():
    user_app = UserApp(
        repo=UserRepoMock(),
        auth=DummyProvider(),
    )

    user_id = await user_app.create_user(
        UserCreateBody(
            username="TestUser",
            password="Password",
        )
    )
    assert user_id == 123
