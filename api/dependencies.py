from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from core.factories.use_case_factory import UseCaseFactory
from core.infra.sqlalchemy.user_repository import UserRepository
from core.infra.sqlalchemy.product_repository import ProductRepository
from core.infra.sqlalchemy.order_repository import OrderRepository
from core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_use_case_factory(db: AsyncSession = Depends(get_db)) -> UseCaseFactory:
    user_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    order_repo = OrderRepository(db)
    
    return UseCaseFactory(
        user_repository=user_repo,
        product_repository=product_repo,
        order_repository=order_repo
    )

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    find_user = factory.create_find_user()
    user = await find_user.execute(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user