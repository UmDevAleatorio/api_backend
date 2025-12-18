import pytest

from core.domain.entities.product import Product
from core.domain.entities.user import User
from core.domain.use_cases.create_order import CreateOrder
from core.domain.value_objects import Email, Name, Password, Photo, Price
from core.infra.mocks import (
    MockOrderRepository,
    MockProductRepository,
    MockUserRepository,
)


@pytest.mark.asyncio
async def test_create_order_success():
    user_repo = MockUserRepository()
    prod_repo = MockProductRepository()
    order_repo = MockOrderRepository()

    # Setup: Criar Usuário e Produto no banco falso
    user = User("u1", Name("User"), Email("u@u.com"), Password("Password123!"))
    await user_repo.save(user)

    # Produto com estoque 10
    prod = Product(
        "p1",
        Name("Brita"),
        Price(50.0),
        Photo("http://teste.com/img.jpg"),
        stock=10,
        user_id="u1",
    )
    await prod_repo.save(prod)

    use_case = CreateOrder(user_repo, prod_repo, order_repo)

    # Executa: Compra 2 unidades
    order = await use_case.execute(order_id="o1", user_id="u1", items_data=[("p1", 2)])

    assert order.total_price.value == 100.0

    saved_prod = await prod_repo.find_by_id("p1")
    assert saved_prod.stock == 8
