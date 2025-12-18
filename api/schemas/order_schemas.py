from datetime import datetime
from typing import Any, List

from pydantic import BaseModel, ConfigDict, field_validator


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    sub_total: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator("unit_price", "sub_total", mode="before")
    @classmethod
    def extract_value_object(cls, v: Any) -> Any:
        if hasattr(v, "value"):
            return v.value
        return v


class OrderResponse(BaseModel):
    id: str
    user_id: str
    total_price: float
    order_date: datetime
    status: str
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("total_price", mode="before")
    @classmethod
    def extract_value_object(cls, v: Any) -> Any:
        if hasattr(v, "value"):
            return v.value
        return v


class OrderUpdate(BaseModel):
    status: str
