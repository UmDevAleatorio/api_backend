from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    products = relationship("ProductModel", back_populates="user")
    orders = relationship("OrderModel", back_populates="user")