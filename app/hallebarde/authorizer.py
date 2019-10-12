import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event: dict, context) -> dict:
    logging.info('Processing event ' + str(event))
    token = event['authorizationToken']
    method_arn = event['methodArn']

    auth_response = {'principalId': 'hallebarde_authorizer',
                     'policyDocument': generate_policy(validate(token), method_arn)}

    return auth_response


def validate(token: str) -> bool:
    if token == 'valid':
        return True
    else:
        return False


def generate_policy(is_valid: bool, resource: str) -> dict:
    policy = {}

    policy['Version'] = '2012-10-17'
    statement = {'Action': 'execute-api:Invoke',
                 'Effect': 'Allow' if is_valid else 'Deny',
                 'Resource': resource}
    policy['Statement'] = [statement]
    return policy
