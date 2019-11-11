import json
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import event_parser
from hallebarde import config


def handle(event: dict, context: dict) -> dict:
    jwt_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    sub = event_parser.extract_sub_from_jwt(jwt_token)

    exchanges = exchange_repository.get_account_exchanges(sub)
    return {
        "isBase64Encoded": False,
        "body": json.dumps([exchange.__dict__ for exchange in exchanges]),
        "headers": None,
        "statusCode": 200
    }
