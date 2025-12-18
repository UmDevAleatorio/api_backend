import dataclasses


@dataclasses.dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not self.validate(self.value):
            raise ValueError("Invalid name")

    @staticmethod
    def validate(name: str) -> bool:
        return len(name) > 0
