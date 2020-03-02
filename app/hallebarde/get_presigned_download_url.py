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

BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'


def handle(event: dict, context: dict) -> Optional[dict]:
    s3_client = boto3.client('s3')

    download_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    identifier = exchange_repository.get_identifier_from_token(download_token=download_token)
    key = file_repository.get_file(identifier)

    if key:
        try:
            response = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': key})
        except ClientError as e:
            logging.error(e)
            return _generate_response("Internal Error", HTTPStatus.INTERNAL_SERVER_ERROR)
        return _generate_response(response, HTTPStatus.OK)
    else:
        return _generate_response("No file associated to this token", HTTPStatus.NOT_FOUND)


def _generate_response(url: str, status_code: int):
    return {
        "isBase64Encoded": False,
        "body": url,
        "headers": None,
        "statusCode": status_code
    }
