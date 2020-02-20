import logging

from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import file_repository
from hallebarde.infrastructure.event_parser import extract_from_headers

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    identifier = extract_from_headers('exchange_identifier', event)

    file_repository.delete_files(identifier)
    exchange_repository.delete(identifier)

    return {
        "isBase64Encoded": False,
        "body": None,
        "headers": None,
        "statusCode": 200
    }
