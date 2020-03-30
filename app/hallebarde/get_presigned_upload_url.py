import json
import logging
from http import HTTPStatus
from typing import Optional

import boto3
from botocore.exceptions import ClientError

import hallebarde.config
from hallebarde import config
from hallebarde.infrastructure import event_parser
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import file_repository
from hallebarde.responses.endpoint_responses import generate_response

BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> Optional[dict]:
    s3_client = boto3.client('s3')
    upload_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    logger.info(f'Extracted upload_token from headers: {upload_token}')
    identifier = exchange_repository.get_identifier_from_token(upload_token=upload_token)
    logger.info(f'Queried identifier from repository: {identifier}')
    filename = event_parser.extract_from_headers('filename', event)
    logger.info(f'Extracted filename from headers: {filename}')

    if _check_if_a_file_exists(identifier):
        return generate_response('A file already exists for this identifier', HTTPStatus.CONFLICT)
    else:
        try:
            response = s3_client.generate_presigned_post(
                BUCKET_NAME,
                _generate_key(identifier, filename),
                Fields=None,
                Conditions=None,
                ExpiresIn=600
            )
        except ClientError as e:
            logging.error(e)
            return generate_response('Internal error', HTTPStatus.INTERNAL_SERVER_ERROR)

        exchange_repository.revoke_upload(identifier)
        return generate_response(json.dumps(response), HTTPStatus.OK)


def _generate_key(identifier: str, filename: str) -> str:
    return f'{identifier}/{filename}'


def _check_if_a_file_exists(identifier: str) -> bool:
    return True if file_repository.get_file(identifier) is not None else False