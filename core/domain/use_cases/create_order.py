import dataclasses
from typing import List, Tuple

from ..entities.order import Order
from ..entities.order_item import OrderItem
from ..repositories.i_order_repository import IOrderRepository
from ..repositories.i_product_repository import IProductRepository
from ..repositories.i_user_repository import IUserRepository

@dataclasses.dataclass
class CreateOrder:
    user_repository: IUserRepository
    product_repository: IProductRepository
    order_repository: IOrderRepository

    # items_data é uma lista de tuplas (product_id, quantity)
    async def execute(self, order_id: str, user_id: str, items_data: List[Tuple[str, int]]) -> Order:
        # 1. Valida Usuário
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        order_items = []

        # 2. Processa cada item do pedido
        for product_id, quantity in items_data:
            product = await self.product_repository.find_by_id(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            
            # Valida e baixa estoque na memória (o método decrease_stock que criamos na Entidade)
            # Nota: Em um sistema real, isso precisaria de transações de banco de dados para evitar condição de corrida
            updated_product = product.decrease_stock(quantity)
            
            # Atualiza o produto no banco com o novo estoque
            await self.product_repository.update(updated_product)

            # Cria a entidade do item
            item = OrderItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                product=updated_product
            )
            order_items.append(item)

        # 3. Cria o Pedido (o cálculo do total é feito automaticamente na entidade Order)
        order = Order.create(
            id=order_id,
            user_id=user_id,
            items=order_items
        )

        # 4. Salva o Pedido
        await self.order_repository.save(order)
        return order