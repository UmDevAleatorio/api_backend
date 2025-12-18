from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    photo = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="products")
