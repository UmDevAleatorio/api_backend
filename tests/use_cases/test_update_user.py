import pytest

from core.domain.use_cases.register_user import RegisterUser
from core.domain.use_cases.update_user import UpdateUser
from core.infra.mocks.mock_user_repository import MockUserRepository


@pytest.mark.asyncio
async def test_should_update_a_user():
    user_repository = MockUserRepository()
    register_user = RegisterUser(user_repository)
    update_user = UpdateUser(user_repository)

    user = await register_user.execute("Test User", "test@example.com", "ValidPass1!")
    updated_user = await update_user.execute(
        user.id, name="Updated Name", email="updated@example.com"
    )

    assert updated_user.name.value == "Updated Name"
    assert updated_user.email.value == "updated@example.com"


@pytest.mark.asyncio
async def test_should_not_update_a_non_existent_user():
    user_repository = MockUserRepository()
    update_user = UpdateUser(user_repository)

    with pytest.raises(ValueError, match="User not found"):
        await update_user.execute("non-existent-id", name="Updated Name")
