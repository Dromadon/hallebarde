from secrets import token_urlsafe
from uuid import uuid4


class Exchange:
    identifier: str
    upload_token: str
    download_token: str
    email: str

    def __init__(self, identifier, email, upload_token, download_token, revoked_upload=False):
        self.revoked_upload = revoked_upload
        self.identifier = identifier
        self.email = email
        self.upload_token = upload_token
        self.download_token = download_token

    @classmethod
    def generate(cls, email: str):
        return cls(
            identifier=str(uuid4()),
            email=email,
            upload_token=token_urlsafe(32),
            download_token=token_urlsafe(32)
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier \
                and self.upload_token == other.upload_token \
                and self.download_token == other.download_token \
                and self.email == other.email \
                and self.revoked_upload == other.revoked_upload
        return False
