import pytest
from core.domain.use_cases.create_product import CreateProduct
from core.infra.mocks.mock_product_repository import MockProductRepository

@pytest.mark.asyncio
async def test_create_product_success():
    repo = MockProductRepository()
    use_case = CreateProduct(repo)
    
    result = await use_case.execute(
        id="p1", name="Areia", price=100.0, photo="http://test.com/img.jpg", stock=50, user_id="u1"
    )
    
    assert result.name.value == "Areia"
    saved = await repo.find_by_id("p1")
    assert saved is not None