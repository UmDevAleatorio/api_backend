import pytest

from core.domain.use_cases.find_user import FindUser
from core.domain.use_cases.register_user import RegisterUser
from core.infra.mocks.mock_user_repository import MockUserRepository


@pytest.mark.asyncio
async def test_should_find_a_user_by_id():
    user_repository = MockUserRepository()
    register_user = RegisterUser(user_repository)
    find_user = FindUser(user_repository)

    user = await register_user.execute("Test User", "test@example.com", "ValidPass1!")
    found_user = await find_user.execute(user.id)

    assert found_user is not None
    assert found_user.id == user.id


@pytest.mark.asyncio
async def test_should_return_none_if_user_not_found():
    user_repository = MockUserRepository()
    find_user = FindUser(user_repository)

    found_user = await find_user.execute("non-existent-id")

    assert found_user is None
