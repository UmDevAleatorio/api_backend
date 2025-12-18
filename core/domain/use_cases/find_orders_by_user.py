import dataclasses
from typing import List

from ..entities.order import Order
from ..repositories.i_order_repository import IOrderRepository

@dataclasses.dataclass
class FindOrdersByUser:
    repository: IOrderRepository

    async def execute(self, user_id: str) -> List[Order]:
        return await self.repository.find_by_user_id(user_id)