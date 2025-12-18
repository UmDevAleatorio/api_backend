import pytest
from datetime import datetime
from core.domain.use_cases.delete_order import DeleteOrder
from core.infra.mocks.mock_order_repository import MockOrderRepository
from core.infra.mocks.mock_product_repository import MockProductRepository
from core.domain.entities.order import Order
from core.domain.entities.order_item import OrderItem
from core.domain.entities.product import Product
from core.domain.value_objects import Name, Price, Photo

@pytest.mark.asyncio
async def test_delete_order_restores_stock():
    order_repo = MockOrderRepository()
    product_repo = MockProductRepository()

    product = Product("p1", Name("Furadeira"), Price(100.0), Photo("http://test.com/img.jpg"), 0, "u1")
    await product_repo.save(product)
    
    item = OrderItem("p1", 2, Price(100.0))
    order = Order("o1", "u1", [item], Price(200.0), datetime.now(), "Processando")
    await order_repo.save(order)

    use_case = DeleteOrder(order_repo, product_repo)
    await use_case.execute("o1")

    assert await order_repo.find_by_id("o1") is None
    updated_prod = await product_repo.find_by_id("p1")
    assert updated_prod.stock == 2