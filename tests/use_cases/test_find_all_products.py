import pytest
from core.domain.use_cases.find_all_products import FindAllProducts
from core.infra.mocks.mock_product_repository import MockProductRepository
from core.domain.entities.product import Product
from core.domain.value_objects import Name, Price, Photo

@pytest.mark.asyncio
async def test_find_all_products():
    repo = MockProductRepository()
    p1 = Product("1", Name("Cimento"), Price(20.0), Photo("http://test.com/img1.jpg"), 10, "u1")
    p2 = Product("2", Name("Areia"), Price(50.0), Photo("http://test.com/img2.jpg"), 5, "u1")
    await repo.save(p1)
    await repo.save(p2)

    use_case = FindAllProducts(repo)
    result = await use_case.execute()

    assert len(result) == 2