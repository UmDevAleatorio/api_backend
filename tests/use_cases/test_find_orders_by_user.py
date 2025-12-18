import pytest
from datetime import datetime
from core.domain.use_cases.find_orders_by_user import FindOrdersByUser
from core.infra.mocks.mock_order_repository import MockOrderRepository
from core.domain.entities.order import Order
from core.domain.value_objects import Price

@pytest.mark.asyncio
async def test_find_orders_by_user():
    repo = MockOrderRepository()
    # Cria 2 pedidos para o usuario u1 e 1 para u2
    o1 = Order("o1", "u1", [], Price(10.0), datetime.now(), "Processando")
    o2 = Order("o2", "u1", [], Price(20.0), datetime.now(), "Enviado")
    o3 = Order("o3", "u2", [], Price(30.0), datetime.now(), "Processando")
    
    await repo.save(o1)
    await repo.save(o2)
    await repo.save(o3)

    use_case = FindOrdersByUser(repo)
    result = await use_case.execute("u1")

    assert len(result) == 2
    # Garante que pegou os pedidos certos
    ids = [o.id for o in result]
    assert "o1" in ids
    assert "o2" in ids