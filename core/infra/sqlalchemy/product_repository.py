from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.product import Product
from ...domain.value_objects import Name, Photo, Price
from ...domain.repositories.i_product_repository import IProductRepository
from ..orm.product import ProductModel


class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, product: Product) -> None:
        product_model = ProductModel(
            id=product.id,
            name=product.name.value,
            price=product.price.value,
            photo=product.photo.value,
            stock=product.stock,
            user_id=product.user_id,
        )
        self.session.add(product_model)
        await self.session.commit()

    async def find_by_id(self, id: str) -> Optional[Product]:
        query = select(ProductModel).where(ProductModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()
        
        if not model:
            return None
            
        return Product(
            id=model.id,
            name=Name(model.name),
            price=Price(model.price),
            photo=Photo(model.photo),
            stock=model.stock,
            user_id=model.user_id
        )

    async def find_all(self) -> List[Product]:
        query = select(ProductModel)
        result = await self.session.execute(query)
        models = result.scalars().all()
        
        return [
            Product(
                id=m.id,
                name=Name(m.name),
                price=Price(m.price),
                photo=Photo(m.photo),
                stock=m.stock,
                user_id=m.user_id
            )
            for m in models
        ]

    async def update(self, product: Product) -> None:
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model:
            model.name = product.name.value
            model.price = product.price.value
            model.photo = product.photo.value
            model.stock = product.stock
            await self.session.commit()

    async def delete(self, id: str) -> None:
        query = select(ProductModel).where(ProductModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model:
            await self.session.delete(model)
            await self.session.commit()