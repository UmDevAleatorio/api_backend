from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ProductBase(BaseModel):
    name: str
    price: float
    photo: str
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    photo: Optional[str] = None
    stock: Optional[int] = None


class ProductResponse(ProductBase):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name", "price", "photo", mode="before")
    @classmethod
    def extract_value_object(cls, v: Any) -> Any:
        if hasattr(v, "value"):
            return v.value
        return v
