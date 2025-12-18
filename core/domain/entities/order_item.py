import dataclasses

from ..value_objects import Price
from .product import Product


@dataclasses.dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: Price
    product: Product | None = None

    @property
    def sub_total(self) -> Price:
        return Price(self.unit_price.value * self.quantity)
