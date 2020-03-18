def generate_aws_policy(is_valid: bool, resource: str) -> dict:
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': 'Allow' if is_valid else 'Deny',
            'Resource': resource
        }]
    }


def generate_response(principal_id: str, policy_document: dict) -> dict:
    return {
        'principalId': principal_id,
        'policyDocument': policy_document
    }
