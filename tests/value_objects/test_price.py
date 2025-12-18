import pytest

from core.domain.value_objects.price import Price


def test_price_valid():
    price = Price(10.0)
    assert price.value == 10.0


def test_price_zero():
    price = Price(0.0)
    assert price.value == 0.0


def test_price_negative():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Price(-1.0)


def test_price_addition():
    p1 = Price(10.0)
    p2 = Price(20.0)
    p3 = p1 + p2
    assert p3.value == 30.0
