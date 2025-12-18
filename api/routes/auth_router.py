from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_use_case_factory
from api.schemas.user_schemas import LoginResponse, UserCreate, UserResponse
from core.factories.use_case_factory import UseCaseFactory
from core.security import create_access_token, get_password_hash, verify_password

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    factory: UseCaseFactory = Depends(get_use_case_factory),
) -> Any:
    find_user = factory.create_find_user_by_email()
    user = await find_user.execute(form_data.username)

    if not user:
        print(f"DEBUG: Login falhou. Usuário {form_data.username} não achado.")

    if not user or not verify_password(form_data.password, user.password.value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Gera Token
    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name.value,
    }


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate, factory: UseCaseFactory = Depends(get_use_case_factory)
):
    register_user = factory.create_register_user()
    try:
        hashed_password = get_password_hash(user_data.password)

        new_user = await register_user.execute(
            name=user_data.name, email=user_data.email, password=hashed_password
        )
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
