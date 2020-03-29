import json
from http import HTTPStatus

from hallebarde import config
from hallebarde.infrastructure import event_parser
from hallebarde.infrastructure import exchange_repository
from hallebarde.responses.endpoint_responses import generate_response


def handle(event: dict, context: dict) -> dict:
    jwt_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    sub = event_parser.extract_sub_from_jwt(jwt_token)

    exchanges = exchange_repository.get_account_exchanges(sub)
    return generate_response(json.dumps([exchange.__dict__ for exchange in exchanges], default=str), HTTPStatus.OK)
