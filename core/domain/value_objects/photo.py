import dataclasses
from urllib.parse import urlparse


@dataclasses.dataclass(frozen=True)
class Photo:
    url: str

    def __post_init__(self):
        if not self.validate(self.url):
            raise ValueError("Invalid photo URL")

    @staticmethod
    def validate(url: str) -> bool:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
