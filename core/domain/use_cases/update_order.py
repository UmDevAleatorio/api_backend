import dataclasses
from typing import Optional
from ..entities.order import Order
from ..repositories.i_order_repository import IOrderRepository

@dataclasses.dataclass
class UpdateOrder:
    repository: IOrderRepository

    async def execute(self, id: str, new_status: str) -> Optional[Order]:
        order = await self.repository.find_by_id(id)
        if not order:
            raise ValueError("Order not found")

        updated_order = order.update_status(new_status)
        
        await self.repository.update(updated_order)
        return updated_order