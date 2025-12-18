import dataclasses
from typing import Optional

from ..entities.product import Product
from ..repositories.i_product_repository import IProductRepository
from ..value_objects import Name, Photo, Price

@dataclasses.dataclass
class UpdateProduct:
    repository: IProductRepository

    async def execute(self, id: str, name: str, price: float, photo: str, stock: int) -> Optional[Product]:
        product = await self.repository.find_by_id(id)
        if not product:
            return None

        # Cria uma nova instância com os dados atualizados (imutabilidade)
        updated_product = dataclasses.replace(
            product,
            name=Name(name),
            price=Price(price),
            photo=Photo(photo),
            stock=stock
        )
        
        await self.repository.update(updated_product)
        return updated_product