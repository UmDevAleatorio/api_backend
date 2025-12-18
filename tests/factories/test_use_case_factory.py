from core.domain.use_cases import (
    CreateOrder,
    CreateProduct,
    DeleteOrder,
    DeleteProduct,
    DeleteUser,
    FindAllProducts,
    FindOrdersByUser,
    FindProductById,
    FindUser,
    FindUserByEmail,
    LoginUser,
    RegisterUser,
    UpdateOrder,
    UpdateProduct,
    UpdateUser,
)
from core.factories.use_case_factory import UseCaseFactory
from core.infra.mocks import (
    MockOrderRepository,
    MockProductRepository,
    MockUserRepository,
)


def test_use_case_factory_initialization():
    factory = UseCaseFactory()
    assert isinstance(factory.user_repository, MockUserRepository)
    assert isinstance(factory.product_repository, MockProductRepository)
    assert isinstance(factory.order_repository, MockOrderRepository)


def test_create_user_use_cases():
    factory = UseCaseFactory()
    assert isinstance(factory.create_register_user(), RegisterUser)
    assert isinstance(factory.create_login_user(), LoginUser)
    assert isinstance(factory.create_find_user(), FindUser)
    assert isinstance(factory.create_find_user_by_email(), FindUserByEmail)
    assert isinstance(factory.create_update_user(), UpdateUser)
    assert isinstance(factory.create_delete_user(), DeleteUser)


def test_create_product_use_cases():
    factory = UseCaseFactory()
    assert isinstance(factory.create_create_product(), CreateProduct)
    assert isinstance(factory.create_find_all_products(), FindAllProducts)
    assert isinstance(factory.create_find_product_by_id(), FindProductById)
    assert isinstance(factory.create_update_product(), UpdateProduct)
    assert isinstance(factory.create_delete_product(), DeleteProduct)


def test_create_order_use_cases():
    factory = UseCaseFactory()
    assert isinstance(factory.create_create_order(), CreateOrder)
    assert isinstance(factory.create_find_orders_by_user(), FindOrdersByUser)
    assert isinstance(factory.create_delete_order(), DeleteOrder)
    assert isinstance(factory.create_update_order(), UpdateOrder)
