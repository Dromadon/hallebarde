from dataclasses import dataclass
from secrets import token_urlsafe
from uuid import uuid4


@dataclass
class Exchange:
    identifier: str
    upload_token: str
    download_token: str

    @classmethod
    def generate(cls):
        return cls(
            identifier=str(uuid4()),
            upload_token=token_urlsafe(32),
            download_token=token_urlsafe(32)
        )
