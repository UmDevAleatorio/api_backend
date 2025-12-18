import dataclasses

from ..repositories.i_product_repository import IProductRepository


@dataclasses.dataclass
class DeleteProduct:
    repository: IProductRepository

    async def execute(self, id: str) -> None:
        await self.repository.delete(id)
