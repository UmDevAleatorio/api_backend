import pytest

from core.domain.entities.product import Product
from core.domain.use_cases.find_product_by_id import FindProductById
from core.domain.value_objects import Name, Photo, Price
from core.infra.mocks.mock_product_repository import MockProductRepository


@pytest.mark.asyncio
async def test_find_product_by_id_success():
    repo = MockProductRepository()
    product = Product(
        "1", Name("Tijolo"), Price(1.0), Photo("http://test.com/img.jpg"), 100, "u1"
    )
    await repo.save(product)

    use_case = FindProductById(repo)
    result = await use_case.execute("1")

    assert result is not None
    assert result.name.value == "Tijolo"


@pytest.mark.asyncio
async def test_find_product_by_id_not_found():
    repo = MockProductRepository()
    use_case = FindProductById(repo)

    result = await use_case.execute("999")
    assert result is None
