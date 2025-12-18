import dataclasses
from datetime import datetime
from typing import List, Optional

from ..value_objects import Price
from .order_item import OrderItem

@dataclasses.dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem]
    total_price: Price
    order_date: datetime
    status: str = 'Processando' # 'Processando' | 'Enviado' | 'Entregue' | 'Cancelado'

    @classmethod
    def create(cls, id: str, user_id: str, items: List[OrderItem]) -> "Order":
        if not items:
            raise ValueError("Um pedido não pode ser criado sem itens.")
        
        total = sum(item.sub_total.value for item in items)
        
        return cls(
            id=id,
            user_id=user_id,
            items=items,
            total_price=Price(total),
            order_date=datetime.now(),
            status='Processando'
        )
    
    def update_status(self, new_status: str) -> "Order":
        valid_statuses = ['Processando', 'Enviado', 'Entregue', 'Cancelado']
        if new_status not in valid_statuses:
            raise ValueError(f"Status inválido: {new_status}")
        
        return dataclasses.replace(self, status=new_status)