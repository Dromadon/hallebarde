import logging
import secrets

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    body = {
        "upload_token": generate_token(),
        "download_token": generate_token()
    }

    return {
        "isBase64Encoded": False,
        "body": body,
        "headers": None,
        "statusCode": 200
    }


def generate_token() -> str:
    return secrets.token_urlsafe(32)
