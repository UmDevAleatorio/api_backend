from typing import List, Optional

from ...domain.entities.order import Order
from ...domain.repositories.i_order_repository import IOrderRepository


class MockOrderRepository(IOrderRepository):
    def __init__(self):
        self.orders = {}

    async def save(self, order: Order) -> None:
        self.orders[order.id] = order

    async def find_by_id(self, id: str) -> Optional[Order]:
        return self.orders.get(id)

    async def find_by_user_id(self, user_id: str) -> List[Order]:
        return [order for order in self.orders.values() if order.user_id == user_id]

    async def update(self, order: Order) -> None:
        if order.id in self.orders:
            self.orders[order.id] = order
            
    async def delete(self, id: str) -> None:
        if id in self.orders:
            del self.orders[id]