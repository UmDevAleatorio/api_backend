from typing import List, Optional

from ...domain.entities.product import Product
from ...domain.repositories.i_product_repository import IProductRepository


class MockProductRepository(IProductRepository):
    def __init__(self):
        self.products = {}

    async def save(self, product: Product) -> Product:
        self.products[product.id] = product
        return product

    async def find_all(self) -> List[Product]:
        return list(self.products.values())

    async def find_by_id(self, id: str) -> Optional[Product]:
        return self.products.get(id)

    async def update(self, product: Product) -> Optional[Product]:
        if product.id in self.products:
            self.products[product.id] = product
            return product
        return None

    async def delete(self, id: str) -> bool:
        if id in self.products:
            del self.products[id]
            return True
        return False
