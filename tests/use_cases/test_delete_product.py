import pytest

from core.domain.entities.product import Product
from core.domain.use_cases.delete_product import DeleteProduct
from core.domain.value_objects import Name, Photo, Price
from core.infra.mocks.mock_product_repository import MockProductRepository


@pytest.mark.asyncio
async def test_delete_product():
    repo = MockProductRepository()
    product = Product(
        "1", Name("Piso"), Price(50.0), Photo("http://test.com/img.jpg"), 10, "u1"
    )
    await repo.save(product)

    use_case = DeleteProduct(repo)
    await use_case.execute("1")

    saved = await repo.find_by_id("1")
    assert saved is None
