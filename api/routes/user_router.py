from fastapi import APIRouter, Depends, HTTPException, status

from core.factories.use_case_factory import UseCaseFactory

from ..dependencies import get_current_user, get_use_case_factory
from ..schemas.user_schemas import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=UserResponse)
async def find_user_by_id(
    id: str, factory: UseCaseFactory = Depends(get_use_case_factory)
):
    use_case = factory.create_find_user()
    user = await use_case.execute(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current_user=Depends(get_current_user),
    factory: UseCaseFactory = Depends(get_use_case_factory),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this user"
        )

    use_case = factory.create_delete_user()
    await use_case.execute(id)
