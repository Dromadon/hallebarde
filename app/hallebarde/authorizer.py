import logging

from hallebarde.infrastructure import exchange_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context) -> dict:
    logging.info('Processing event %s', str(event))
    token = event['authorizationToken']
    method_arn = event['methodArn']

    return {
        'principalId': 'hallebarde_authorizer',
        'policyDocument': generate_policy(validate(token), method_arn)
    }


def validate(upload_token: str) -> bool:
    exchange = exchange_repository.get_by_upload_token(upload_token)
    return not exchange.revoked_upload


def generate_policy(is_valid: bool, resource: str) -> dict:
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': 'Allow' if is_valid else 'Deny',
            'Resource': resource
        }]
    }
