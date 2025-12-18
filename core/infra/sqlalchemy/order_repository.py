from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.order import Order
from ...domain.entities.order_item import OrderItem
from ...domain.value_objects import Price
from ...domain.repositories.i_order_repository import IOrderRepository
from ..orm.order import OrderModel
from ..orm.order_item import OrderItemModel


class OrderRepository(IOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, order: Order) -> None:
        # Cria os modelos dos itens
        items_models = [
            OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price.value
            )
            for item in order.items
        ]

        order_model = OrderModel(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price.value,
            order_date=order.order_date,
            status=order.status,
            items=items_models # O SQLAlchemy salva os itens automaticamente devido ao relacionamento
        )
        
        self.session.add(order_model)
        await self.session.commit()

    async def find_by_id(self, id: str) -> Optional[Order]:
        # Precisamos carregar os items junto (selectinload)
        query = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return None

        return self._to_entity(model)

    async def find_by_user_id(self, user_id: str) -> List[Order]:
        query = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.user_id == user_id)
        result = await self.session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(m) for m in models]

    async def update(self, order: Order) -> None:
        query = select(OrderModel).where(OrderModel.id == order.id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model:
            model.status = order.status
            # Nota: Atualizar itens é mais complexo, por enquanto focamos no status
            await self.session.commit()
            
    async def delete(self, id: str) -> None:
        query = select(OrderModel).where(OrderModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()
        
        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_entity(self, model: OrderModel) -> Order:
        items = [
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=Price(item.unit_price)
            )
            for item in model.items
        ]
        
        return Order(
            id=model.id,
            user_id=model.user_id,
            items=items,
            total_price=Price(model.total_price),
            order_date=model.order_date,
            status=model.status
        )