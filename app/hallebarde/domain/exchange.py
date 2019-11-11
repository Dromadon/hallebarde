from secrets import token_urlsafe
from uuid import uuid4


class Exchange:
    identifier: str
    upload_token: str
    download_token: str
    sub: str
    revoked_upload: bool

    def __init__(self, identifier: str, sub: str, upload_token: str, download_token: str, revoked_upload: bool = False):
        self.revoked_upload = revoked_upload
        self.identifier = identifier
        self.sub = sub
        self.upload_token = upload_token
        self.download_token = download_token

    @classmethod
    def generate(cls, sub: str):
        return cls(
            identifier=str(uuid4()),
            sub=sub,
            upload_token=token_urlsafe(32),
            download_token=token_urlsafe(32),
            revoked_upload=False
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier \
                   and self.upload_token == other.upload_token \
                   and self.download_token == other.download_token \
                   and self.sub == other.sub \
                   and self.revoked_upload == other.revoked_upload
        return False
