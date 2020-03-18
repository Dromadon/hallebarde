import logging

from hallebarde.infrastructure import exchange_repository
from hallebarde.responses import authorizer_responses

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context: dict) -> dict:
    logging.info('Processing event %s', str(event))
    token = event['authorizationToken']
    method_arn = event['methodArn']

    validation = validate(token)
    logger.info(f'Validation is {validation}')
    policy = authorizer_responses.generate_aws_policy(validation, method_arn)
    return authorizer_responses.generate_response('hallebarde_download_authorizer', policy)


def validate(upload_token: str) -> bool:
    exchange = exchange_repository.get_by_download_token(upload_token)
    return True if exchange else False
