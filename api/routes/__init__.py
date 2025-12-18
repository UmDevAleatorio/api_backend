from .auth_router import router as auth_router
from .order_router import router as order_router
from .product_router import router as product_router
from .user_router import router as user_router

__all__ = ["auth_router", "user_router", "product_router", "order_router"]
