from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.order import Order

class IOrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Order]:
        pass

    @abstractmethod
    async def update(self, order: Order) -> None:
        pass