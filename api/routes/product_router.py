from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import uuid4

from ..dependencies import get_use_case_factory, get_current_user
from ..schemas.product_schemas import ProductCreate, ProductResponse, ProductUpdate
from core.factories.use_case_factory import UseCaseFactory

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_create_product()
    try:
        new_product = await use_case.execute(
            id=str(uuid4()),
            name=product.name,
            price=product.price,
            photo=product.photo,
            stock=product.stock,
            user_id=current_user.id
        )
        return new_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProductResponse])
async def find_all_products(
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_find_all_products()
    return await use_case.execute()

@router.get("/{id}", response_model=ProductResponse)
async def find_product_by_id(
    id: str,
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_find_product_by_id()
    product = await use_case.execute(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: str,
    data: ProductUpdate,
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_update_product()
    
    updated_product = await use_case.execute(
        id=id,
        name=data.name or "", 
        price=data.price or 0.0,
        photo=data.photo or "",
        stock=data.stock or 0
    )
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    return updated_product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: str,
    current_user = Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_delete_product()
    await use_case.execute(id)