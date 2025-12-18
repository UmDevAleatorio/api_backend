from core.domain.entities.order import Order
from core.domain.entities.order_item import OrderItem
from core.domain.entities.product import Product
from core.domain.value_objects import Name, Photo, Price


def test_create_order_calculates_total():
    prod = Product(
        "p1", Name("Tijolo"), Price(2.0), Photo("http://img.com/foto.jpg"), 100, "u1"
    )

    item = OrderItem(product_id="p1", quantity=5, unit_price=Price(2.0), product=prod)

    order = Order.create(id="o1", user_id="u1", items=[item])

    assert order.total_price.value == 10.0
    assert order.status == "Processando"
    assert len(order.items) == 1
