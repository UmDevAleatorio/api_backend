import pytest

from core.domain.use_cases.delete_user import DeleteUser
from core.domain.use_cases.register_user import RegisterUser
from core.infra.mocks.mock_user_repository import MockUserRepository


@pytest.mark.asyncio
async def test_should_delete_a_user():
    user_repository = MockUserRepository()
    register_user = RegisterUser(user_repository)
    delete_user = DeleteUser(user_repository)

    user = await register_user.execute("Test User", "test@example.com", "ValidPass1!")
    await delete_user.execute(user.id)

    assert len(user_repository.users) == 0


@pytest.mark.asyncio
async def test_should_not_delete_a_non_existent_user():
    user_repository = MockUserRepository()
    delete_user = DeleteUser(user_repository)

    with pytest.raises(ValueError, match="User not found"):
        await delete_user.execute("non-existent-id")
