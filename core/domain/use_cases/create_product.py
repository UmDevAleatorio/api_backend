import dataclasses

from ..entities.product import Product
from ..repositories.i_product_repository import IProductRepository
from ..value_objects import Name, Photo, Price


@dataclasses.dataclass
class CreateProduct:
    repository: IProductRepository

    async def execute(
        self, id: str, name: str, price: float, photo: str, stock: int, user_id: str
    ) -> Product:
        product = Product(
            id=id,
            name=Name(name),
            price=Price(price),
            photo=Photo(photo),
            stock=stock,
            user_id=user_id,
        )

        await self.repository.save(product)
        return product
