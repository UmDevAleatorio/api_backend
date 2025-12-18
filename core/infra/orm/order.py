from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(String, default="Processando")

    user = relationship("UserModel", back_populates="orders")
    items = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan"
    )
