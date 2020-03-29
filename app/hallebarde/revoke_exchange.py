import logging
from http import HTTPStatus

from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import file_repository
from hallebarde.usecases import revoke_exchange_command_handler
from hallebarde.infrastructure import event_parser
from hallebarde import config
from hallebarde.responses.endpoint_responses import generate_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    jwt_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    event_sub = event_parser.extract_sub_from_jwt(jwt_token)
    identifier = event_parser.extract_from_headers('exchange_identifier', event)

    exchange = exchange_repository.get(identifier)

    if exchange.sub != event_sub:
        return generate_response("Forbidden", HTTPStatus.FORBIDDEN)
    else:
        revoke_exchange_command_handler.handle(identifier)
        return generate_response("Exchange revoked", HTTPStatus.OK)

