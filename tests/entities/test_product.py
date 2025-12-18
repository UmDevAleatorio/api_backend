import pytest

from core.domain.entities.product import Product
from core.domain.value_objects import Name, Photo, Price


def test_create_product():
    product = Product(
        id="123",
        name=Name("Cimento"),
        price=Price(50.0),
        photo=Photo("http://photo.com/img.jpg"),
        stock=100,
        user_id="user_1",
    )
    assert product.id == "123"
    assert product.name.value == "Cimento"
    assert product.price.value == 50.0
    assert product.stock == 100


def test_decrease_product_stock():
    product = Product(
        id="123",
        name=Name("Cimento"),
        price=Price(50.0),
        photo=Photo("http://photo.com"),
        stock=10,
        user_id="user_1",
    )
    updated = product.decrease_stock(2)
    assert updated.stock == 8


def test_decrease_stock_error():
    product = Product(
        id="123",
        name=Name("Cimento"),
        price=Price(50.0),
        photo=Photo("http://photo.com"),
        stock=1,
        user_id="user_1",
    )
    with pytest.raises(ValueError):
        product.decrease_stock(2)
