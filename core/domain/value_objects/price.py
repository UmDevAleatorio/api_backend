import dataclasses
from typing import Any

@dataclasses.dataclass(frozen=True)
class Price:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Price cannot be negative")

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            return NotImplemented
        return Price(self.value + other.value)