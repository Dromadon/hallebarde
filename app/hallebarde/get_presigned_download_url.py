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

BUCKET_NAME = f'{hallebarde.config.APPLICATION_NAME}-{hallebarde.config.ENVIRONMENT}-storage'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> Optional[dict]:
    s3_client = boto3.client('s3')
    download_token = event_parser.extract_from_headers(config.AUTHORIZATION_HEADER, event)
    logger.info(f'Extracted download_token from headers: {download_token}')
    identifier = exchange_repository.get_identifier_from_token(download_token=download_token)
    logger.info(f'Queried identifier from repository: {identifier}')
    key = file_repository.get_file(identifier)
    logger.info(f'Extracted file key from storage: {key}')

    if key:
        try:
            logger.info("Generating presigned url")
            response = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': key})
        except ClientError as e:
            logging.error(e)
            return generate_response("Internal Error", HTTPStatus.INTERNAL_SERVER_ERROR)
        return generate_response(response, HTTPStatus.OK)
    else:
        return generate_response("No file associated to this token", HTTPStatus.NOT_FOUND)


