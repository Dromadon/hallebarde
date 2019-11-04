import json
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure.event_parser import extract_email_from_headers


def handle(event: dict, context: dict) -> dict:
    email = extract_email_from_headers(event)

    exchanges = exchange_repository.get_account_exchanges(email)
    return {
        "isBase64Encoded": False,
        "body": json.dumps([exchange.__dict__ for exchange in exchanges]),
        "headers": None,
        "statusCode": 200
    }
