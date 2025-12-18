import dataclasses
from typing import Optional

from ..entities.product import Product
from ..repositories.i_product_repository import IProductRepository

@dataclasses.dataclass
class FindProductById:
    repository: IProductRepository

    async def execute(self, id: str) -> Optional[Product]:
        return await self.repository.find_by_id(id)