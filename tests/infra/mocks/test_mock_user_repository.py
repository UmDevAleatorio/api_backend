import pytest
from core.infra.mocks.mock_user_repository import MockUserRepository
from core.domain.entities.user import User
from core.domain.value_objects import Name, Email, Password

VALID_PASS = "Password123!"

@pytest.mark.asyncio
async def test_save_and_find_user():
    repo = MockUserRepository()
    user = User("u1", Name("John"), Email("john@example.com"), Password(VALID_PASS))
    
    await repo.save(user)
    
    found_id = await repo.find_by_id("u1")
    assert found_id == user

@pytest.mark.asyncio
async def test_update_user():
    repo = MockUserRepository()
    user = User("u1", Name("John"), Email("john@example.com"), Password(VALID_PASS))
    await repo.save(user)
    
    updated_user = User("u1", Name("John Doe"), Email("john@example.com"), Password(VALID_PASS))
    await repo.update(updated_user)
    
    found = await repo.find_by_id("u1")
    assert found.name.value == "John Doe"

@pytest.mark.asyncio
async def test_delete_user():
    repo = MockUserRepository()
    user = User("u1", Name("John"), Email("john@example.com"), Password(VALID_PASS))
    await repo.save(user)
    
    await repo.delete("u1")
    
    found = await repo.find_by_id("u1")
    assert found is None