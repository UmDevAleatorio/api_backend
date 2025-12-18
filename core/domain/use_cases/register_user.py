from uuid import uuid4

from ..entities.user import User
from ..repositories.i_user_repository import IUserRepository
from ..value_objects import Email, Name, Password


class RegisterUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, name: str, email: str, password: str) -> User:
        # 1. Verifica se já existe (Resolve o erro "DID NOT RAISE")
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("User already exists")

        # 2. Cria e Salva
        user_id = str(uuid4())
        new_user = User(
            id=user_id, name=Name(name), email=Email(email), password=Password(password)
        )

        await self.user_repository.save(new_user)
        return new_user
