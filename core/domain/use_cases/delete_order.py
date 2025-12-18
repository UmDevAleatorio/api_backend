import dataclasses
from ..repositories.i_order_repository import IOrderRepository
from ..repositories.i_product_repository import IProductRepository

@dataclasses.dataclass
class DeleteOrder:
    order_repository: IOrderRepository
    product_repository: IProductRepository

    async def execute(self, id: str) -> None:
        # 1. Busca o pedido para saber quais itens devolver
        order = await self.order_repository.find_by_id(id)
        if not order:
             # Se não achar, pode lançar erro ou só retornar (depende da sua preferência)
            return

        # 2. Devolve o estoque de cada item
        for item in order.items:
            product = await self.product_repository.find_by_id(item.product_id)
            if product:
                updated_product = product.increase_stock(item.quantity)
                await self.product_repository.update(updated_product)

        # 3. Deleta o pedido
        await self.order_repository.delete(id)