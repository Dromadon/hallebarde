import logging

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


def validate(token: str) -> bool:
    return token == 'valid'


def generate_policy(is_valid: bool, resource: str) -> dict:
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': 'Allow' if is_valid else 'Deny',
            'Resource': resource
        }]
    }
