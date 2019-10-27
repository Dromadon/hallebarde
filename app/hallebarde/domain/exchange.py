from dataclasses import dataclass


@dataclass
class Exchange:
    identifier: str
    upload_token: str
    download_token: str
