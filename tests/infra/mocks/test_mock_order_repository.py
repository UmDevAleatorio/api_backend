from datetime import datetime

import pytest

from core.domain.entities.order import Order
from core.domain.entities.order_item import OrderItem
from core.domain.value_objects import Price
from core.infra.mocks.mock_order_repository import MockOrderRepository


@pytest.mark.asyncio
async def test_save_and_find_order():
    repo = MockOrderRepository()
    # Mock simples dos itens, pois aqui só testamos a persistência do pedido
    item = OrderItem("p1", 2, Price(10.0))
    order = Order("o1", "u1", [item], Price(20.0), datetime.now(), "Processando")

    await repo.save(order)

    found = await repo.find_by_id("o1")
    assert found == order


@pytest.mark.asyncio
async def test_find_orders_by_user():
    repo = MockOrderRepository()
    item = OrderItem("p1", 2, Price(10.0))
    o1 = Order("o1", "u1", [item], Price(20.0), datetime.now(), "Processando")
    o2 = Order("o2", "u1", [item], Price(20.0), datetime.now(), "Enviado")
    o3 = Order("o3", "u2", [item], Price(20.0), datetime.now(), "Processando")

    await repo.save(o1)
    await repo.save(o2)
    await repo.save(o3)

    user_orders = await repo.find_by_user_id("u1")
    assert len(user_orders) == 2
    assert o1 in user_orders
    assert o2 in user_orders
    assert o3 not in user_orders


@pytest.mark.asyncio
async def test_update_order():
    repo = MockOrderRepository()
    item = OrderItem("p1", 2, Price(10.0))
    order = Order("o1", "u1", [item], Price(20.0), datetime.now(), "Processando")
    await repo.save(order)

    updated_order = Order("o1", "u1", [item], Price(20.0), datetime.now(), "Entregue")
    await repo.update(updated_order)

    found = await repo.find_by_id("o1")
    assert found.status == "Entregue"


@pytest.mark.asyncio
async def test_delete_order():
    repo = MockOrderRepository()
    item = OrderItem("p1", 2, Price(10.0))
    order = Order("o1", "u1", [item], Price(20.0), datetime.now(), "Processando")
    await repo.save(order)

    await repo.delete("o1")

    found = await repo.find_by_id("o1")
    assert found is None
