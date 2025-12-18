import pytest

from core.domain.use_cases.find_user_by_email import FindUserByEmail
from core.domain.use_cases.register_user import RegisterUser
from core.infra.mocks.mock_user_repository import MockUserRepository


@pytest.mark.asyncio
async def test_should_find_a_user_by_email():
    user_repository = MockUserRepository()
    register_user = RegisterUser(user_repository)
    find_user_by_email = FindUserByEmail(user_repository)

    await register_user.execute("Test User", "test@example.com", "ValidPass1!")
    found_user = await find_user_by_email.execute("test@example.com")

    assert found_user is not None
    assert found_user.email.value == "test@example.com"


@pytest.mark.asyncio
async def test_should_return_none_if_user_not_found_by_email():
    user_repository = MockUserRepository()
    find_user_by_email = FindUserByEmail(user_repository)

    found_user = await find_user_by_email.execute("non-existent-email@example.com")

    assert found_user is None
