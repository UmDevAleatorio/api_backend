import dataclasses
from typing import List

from ..entities.product import Product
from ..repositories.i_product_repository import IProductRepository

@dataclasses.dataclass
class FindAllProducts:
    repository: IProductRepository

    async def execute(self) -> List[Product]:
        return await self.repository.find_all()