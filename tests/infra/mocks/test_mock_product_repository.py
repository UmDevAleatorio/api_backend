import pytest

from core.domain.entities.product import Product
from core.domain.value_objects import Name, Photo, Price
from core.infra.mocks.mock_product_repository import MockProductRepository

VALID_URL = "http://site.com/img.jpg"


@pytest.mark.asyncio
async def test_save_and_find_product():
    repo = MockProductRepository()
    product = Product("1", Name("Cimento"), Price(25.0), Photo(VALID_URL), 10, "u1")
    await repo.save(product)
    found = await repo.find_by_id("1")
    assert found == product


@pytest.mark.asyncio
async def test_find_all_products():
    repo = MockProductRepository()
    p1 = Product("1", Name("Cimento"), Price(25.0), Photo(VALID_URL), 10, "u1")
    p2 = Product("2", Name("Areia"), Price(50.0), Photo(VALID_URL), 20, "u1")
    await repo.save(p1)
    await repo.save(p2)
    result = await repo.find_all()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_update_product():
    repo = MockProductRepository()
    product = Product("1", Name("Cimento"), Price(25.0), Photo(VALID_URL), 10, "u1")
    await repo.save(product)

    updated_product = Product(
        "1", Name("Novo Nome"), Price(26.0), Photo(VALID_URL), 8, "u1"
    )
    await repo.update(updated_product)
    found = await repo.find_by_id("1")
    assert found.name.value == "Novo Nome"


@pytest.mark.asyncio
async def test_delete_product():
    repo = MockProductRepository()
    product = Product("1", Name("Cimento"), Price(25.0), Photo(VALID_URL), 10, "u1")
    await repo.save(product)
    await repo.delete("1")
    found = await repo.find_by_id("1")
    assert found is None
