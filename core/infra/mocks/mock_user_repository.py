from typing import Optional

from ...domain.entities.user import User
from ...domain.repositories.i_user_repository import IUserRepository


class MockUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    async def save(self, user: User) -> None:
        print(f"DEBUG: Salvando usuário {user.email.value}")  # Debug
        self.users[user.id] = user

    async def find_by_email(self, email: str) -> Optional[User]:
        print(f"DEBUG: Buscando email '{email}' no banco...")  # Debug
        for user in self.users.values():
            stored_email = (
                user.email.value if hasattr(user.email, "value") else str(user.email)
            )

            print(
                f"DEBUG: Comparando '{email}' com armazenado '{stored_email}'"
            )  # Debug

            if stored_email == email:
                print("DEBUG: Usuário ENCONTRADO!")
                return user

        print("DEBUG: Usuário NÃO encontrado.")
        return None

    async def find_by_id(self, id: str) -> Optional[User]:
        return self.users.get(id)

    async def update(self, user: User) -> None:
        if user.id in self.users:
            self.users[user.id] = user

    async def delete(self, id: str) -> None:
        if id in self.users:
            del self.users[id]
