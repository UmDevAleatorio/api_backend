import pytest

from core.domain.entities.product import Product
from core.domain.use_cases.update_product import UpdateProduct
from core.domain.value_objects import Name, Photo, Price
from core.infra.mocks.mock_product_repository import MockProductRepository


@pytest.mark.asyncio
async def test_update_product_success():
    repo = MockProductRepository()
    original = Product(
        "1", Name("Tinta"), Price(100.0), Photo("http://test.com/img.jpg"), 10, "u1"
    )
    await repo.save(original)

    use_case = UpdateProduct(repo)

    updated = await use_case.execute(
        id="1",
        name="Tinta Premium",
        price=120.0,
        photo="http://test.com/img_new.jpg",
        stock=15,
    )

    assert updated.name.value == "Tinta Premium"
    assert updated.price.value == 120.0

    # Verifica persistência
    saved = await repo.find_by_id("1")
    assert saved.name.value == "Tinta Premium"
