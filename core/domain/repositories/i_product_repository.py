from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def update(self, product: Product) -> None:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass
