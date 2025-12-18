import dataclasses
from typing import Optional

from ..value_objects import Name, Photo, Price
from .user import User


@dataclasses.dataclass
class Product:
    id: str
    name: Name
    price: Price
    photo: Photo
    stock: int
    user_id: Optional[str] = None
    user: Optional[User] = None

    def decrease_stock(self, quantity: int) -> "Product":
        if self.stock < quantity:
            raise ValueError(
                f"Estoque insuficiente para o produto '{self.name.value}'."
            )

        return dataclasses.replace(self, stock=self.stock - quantity)

    def increase_stock(self, quantity: int) -> "Product":
        return dataclasses.replace(self, stock=self.stock + quantity)
