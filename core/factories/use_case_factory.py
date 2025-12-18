from typing import Optional

from core.domain.repositories import (
    IOrderRepository,
    IUserRepository,
    IProductRepository,
)
from core.domain.use_cases import (
    # User Use Cases
    DeleteUser,
    FindUser,
    FindUserByEmail,
    LoginUser,
    RegisterUser,
    UpdateUser,
    # Product Use Cases
    CreateProduct,
    DeleteProduct,
    FindAllProducts,
    FindProductById,
    UpdateProduct,
    # Order Use Cases
    CreateOrder,
    DeleteOrder,
    FindOrdersByUser,
    UpdateOrder,
)
from core.infra.mocks import (
    MockOrderRepository,
    MockUserRepository,
    MockProductRepository,
)


class UseCaseFactory:
    def __init__(
        self,
        user_repository: Optional[IUserRepository] = None,
        product_repository: Optional[IProductRepository] = None,
        order_repository: Optional[IOrderRepository] = None,
    ):
        self.user_repository = user_repository or MockUserRepository()
        self.product_repository = (
            product_repository or MockProductRepository()
        )
        self.order_repository = order_repository or MockOrderRepository()

    # --- USER ---
    def create_register_user(self) -> RegisterUser:
        return RegisterUser(user_repository=self.user_repository)

    def create_login_user(self) -> LoginUser:
        return LoginUser(user_repository=self.user_repository)

    def create_find_user(self) -> FindUser:
        return FindUser(user_repository=self.user_repository)

    def create_find_user_by_email(self) -> FindUserByEmail:
        return FindUserByEmail(user_repository=self.user_repository)

    def create_update_user(self) -> UpdateUser:
        return UpdateUser(user_repository=self.user_repository)

    def create_delete_user(self) -> DeleteUser:
        return DeleteUser(user_repository=self.user_repository)

    # --- PRODUCT ---
    def create_create_product(self) -> CreateProduct:
        return CreateProduct(repository=self.product_repository)

    def create_find_product_by_id(self) -> FindProductById:
        return FindProductById(repository=self.product_repository)

    def create_find_all_products(self) -> FindAllProducts:
        return FindAllProducts(repository=self.product_repository)

    def create_update_product(self) -> UpdateProduct:
        return UpdateProduct(repository=self.product_repository)

    def create_delete_product(self) -> DeleteProduct:
        return DeleteProduct(repository=self.product_repository)

    # --- ORDER ---
    def create_create_order(self) -> CreateOrder:
        return CreateOrder(
            order_repository=self.order_repository,
            user_repository=self.user_repository,
            product_repository=self.product_repository,
        )

    def create_find_orders_by_user(self) -> FindOrdersByUser:
        return FindOrdersByUser(repository=self.order_repository)
    
    def create_delete_order(self) -> DeleteOrder:
        return DeleteOrder(
            order_repository=self.order_repository,
            product_repository=self.product_repository
        )
        
    def create_update_order(self) -> UpdateOrder:
        return UpdateOrder(repository=self.order_repository)