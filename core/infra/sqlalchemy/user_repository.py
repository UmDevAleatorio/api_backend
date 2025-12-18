from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...domain.entities.user import User
from ...domain.repositories.i_user_repository import IUserRepository
from ...domain.value_objects import Email, Name, Password
from ..orm.user import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        user_model = UserModel(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            password=user.password.value,
        )
        self.session.add(user_model)
        await self.session.commit()

    async def find_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return None

        return User(
            id=model.id,
            name=Name(model.name),
            email=Email(model.email),
            password=Password(model.password),
        )

    async def find_by_id(self, id: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return None

        return User(
            id=model.id,
            name=Name(model.name),
            email=Email(model.email),
            password=Password(model.password),
        )

    async def update(self, user: User) -> None:
        query = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model:
            model.name = user.name.value
            model.email = user.email.value
            model.password = user.password.value
            await self.session.commit()

    async def delete(self, id: str) -> None:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model:
            await self.session.delete(model)
            await self.session.commit()
