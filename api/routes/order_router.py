from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import uuid4

from ..dependencies import get_use_case_factory, get_current_user
from ..schemas.order_schemas import OrderCreate, OrderResponse, OrderUpdate
from core.factories.use_case_factory import UseCaseFactory

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_create_order()
    try:
        items_tuple = [(item.product_id, item.quantity) for item in order_data.items]
        
        new_order = await use_case.execute(
            order_id=str(uuid4()),
            user_id=current_user.id,
            items_data=items_tuple
        )
        return new_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_find_orders_by_user()
    return await use_case.execute(user_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    id: str,
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_delete_order()
    await use_case.execute(id)