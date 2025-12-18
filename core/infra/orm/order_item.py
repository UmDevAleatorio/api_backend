from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class OrderItemModel(Base):
    __tablename__ = "order_items"

    order_id = Column(String, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), primary_key=True)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")