import dataclasses

from ..value_objects import Email, Name, Password


@dataclasses.dataclass
class User:
    id: str
    name: Name
    email: Email
    password: Password
