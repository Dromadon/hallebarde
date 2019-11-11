import logging
from http import HTTPStatus

from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import file_repository
from hallebarde.infrastructure import event_parser
from hallebarde import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    jwt_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    event_sub = event_parser.extract_sub_from_jwt(jwt_token)
    identifier = event_parser.extract_from_headers('exchange_identifier', event)

    exchange = exchange_repository.get(identifier)

    if exchange.sub != event_sub:
        return _generate_response("Forbidden", HTTPStatus.FORBIDDEN)
    else:
        file_repository.delete_files(identifier)
        exchange_repository.delete(identifier)
        return _generate_response("Exchange revoked", HTTPStatus.OK)


def _generate_response(body: str, status_code: int):
    return {
        "isBase64Encoded": False,
        "body": body,
        "headers": None,
        "statusCode": status_code
    }
