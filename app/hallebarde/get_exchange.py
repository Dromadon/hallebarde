import dataclasses
import json
import logging

from hallebarde.domain.exchange import Exchange
from hallebarde.infrastructure import exchange_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    exchange: Exchange = Exchange.generate()

    exchange_repository.save(exchange)

    return {
        "isBase64Encoded": False,
        "body": json.dumps(dataclasses.asdict(exchange)),
        "headers": None,
        "statusCode": 200
    }
