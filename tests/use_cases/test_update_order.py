import pytest
from datetime import datetime
from core.domain.use_cases.update_order import UpdateOrder
from core.infra.mocks.mock_order_repository import MockOrderRepository
from core.domain.entities.order import Order
from core.domain.value_objects import Price

@pytest.mark.asyncio
async def test_update_order_status():
    repo = MockOrderRepository()
    order = Order("o1", "u1", [], Price(10.0), datetime.now(), "Processando")
    await repo.save(order)

    use_case = UpdateOrder(repo)
    updated = await use_case.execute("o1", "Enviado")

    assert updated.status == "Enviado"
    
    saved = await repo.find_by_id("o1")
    assert saved.status == "Enviado"