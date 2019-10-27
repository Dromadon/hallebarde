import logging
import secrets
import uuid
import json

from hallebarde.domain.exchange import Exchange
from hallebarde.infrastructure import exchange_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    upload_token = generate_token()
    download_token = generate_token()
    identifier = generate_identifier()

    body = {
        "identifier": identifier,
        "upload_token": upload_token,
        "download_token": download_token
    }

    exchange = Exchange(identifier, upload_token, download_token)

    exchange_repository.save(exchange)

    return {
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": None,
        "statusCode": 200
    }


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def generate_identifier() -> str:
    return str(uuid.uuid4())
