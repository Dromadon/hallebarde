import json
import logging

from hallebarde.domain.exchange import Exchange
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import event_parser
from hallebarde import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    jwt = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    sub = event_parser.extract_sub_from_jwt(jwt)

    exchange: Exchange = Exchange.generate(sub)

    exchange_repository.save(exchange)

    return {
        "isBase64Encoded": False,
        "body": json.dumps(exchange.__dict__, default=str),
        "headers": None,
        "statusCode": 200
    }
