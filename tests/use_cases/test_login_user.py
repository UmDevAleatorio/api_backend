import pytest
from core.domain.use_cases.login_user import LoginUser
from core.infra.mocks.mock_user_repository import MockUserRepository
from core.domain.entities.user import User
from core.domain.value_objects import Name, Email, Password
from core.security import get_password_hash

@pytest.mark.asyncio
async def test_should_login_a_user():
    user_repository = MockUserRepository()
    login_user = LoginUser(user_repository)

    hashed_pw = get_password_hash("ValidPass1!")
    
    user = User("u1", Name("Test User"), Email("test@example.com"), Password(hashed_pw))
    await user_repository.save(user)

    result = await login_user.execute("test@example.com", "ValidPass1!")
    
    assert result is not None
    assert result.email.value == "test@example.com"

@pytest.mark.asyncio
async def test_should_not_login_with_invalid_password():
    user_repository = MockUserRepository()
    login_user = LoginUser(user_repository)

    hashed_pw = get_password_hash("ValidPass1!")
    user = User("u1", Name("Test User"), Email("test@example.com"), Password(hashed_pw))
    await user_repository.save(user)

    with pytest.raises(ValueError, match="Invalid credentials"):
        await login_user.execute("test@example.com", "WrongPass")