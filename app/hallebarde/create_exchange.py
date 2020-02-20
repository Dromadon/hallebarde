import json
import logging

from hallebarde.domain.exchange import Exchange
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure.event_parser import extract_from_headers

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    email = extract_from_headers('email', event)

    exchange: Exchange = Exchange.generate(email)

    exchange_repository.save(exchange)

    return {
        "isBase64Encoded": False,
        "body": json.dumps(exchange.__dict__),
        "headers": None,
        "statusCode": 200
    }
