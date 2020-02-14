import json
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError
import hallebarde.config
from hallebarde.infrastructure import exchange_repository
from hallebarde.infrastructure import file_repository
from hallebarde.infrastructure import event_parser

BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'


def handle(event: dict, context: dict) -> Optional[dict]:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    s3_client = boto3.client('s3')
    upload_token = event_parser.extract_upload_token_from_headers(event)
    logger.info(f'Extracted upload_token from headers: {upload_token}')
    identifier = exchange_repository.get_identifier_from_token(upload_token=upload_token)
    logger.info(f'Queried identifier from repository: {identifier}')
    filename = event_parser.extract_filename_from_headers(event)
    logger.info(f'Extracted filename from headers: {filename}')

    if _check_if_a_file_exists(identifier):
        return _generate_response({'error': 'A file already exists for this identifier'}, 409)
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
            return _generate_response({}, 500)

        exchange_repository.revoke_upload(identifier)
        return _generate_response(response, 200)


def _generate_key(identifier: str, filename: str):
    return f'{identifier}/{filename}'


def _check_if_a_file_exists(identifier: str):
    return True if file_repository.get_file(identifier) is not None else False


def _generate_response(body: dict, status_code: int):
    return {
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": None,
        "statusCode": status_code
    }
