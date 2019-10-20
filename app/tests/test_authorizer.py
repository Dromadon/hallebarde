from unittest import TestCase

from hallebarde.authorizer import validate, generate_policy, handle


class TestAuthorizer(TestCase):

    def test_validate_should_return_true_if_token_is_valid(self):
        # When
        response: bool = validate('valid')

        # Then
        assert response is True

    def test_validate_should_return_false_if_token_is_not_valid(self):
        # When
        response: bool = validate('notvalid')

        # Then
        assert response is False

    def test_generate_policy_should_return_a_policy_containing_a_version_and_a_statement(self):
        # When
        policy: dict = generate_policy(is_valid=True, resource='a_resource')

        # Then
        assert 'Version' in policy.keys()
        assert 'Statement' in policy.keys()

    def test_generate_policy_should_return_an_allowed_policy_on_given_resource(self):
        # Given
        policy_validity = True

        # When
        policy: dict = generate_policy(policy_validity, 'arn:aws:fakearn')

        # Then
        assert policy == {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': 'arn:aws:fakearn'
            }]
        }

    def test_generate_policy_should_return_a_denied_policy_on_a_resource_when_invalid(self):
        # Given
        policy_validity = False

        # When
        policy: dict = generate_policy(policy_validity, 'arn:aws:fakearn')

        # Then
        assert policy == {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Deny',
                'Resource': 'arn:aws:fakearn'
            }]
        }

    def test_authorizer_should_return_an_authentication_with_an_id_and_a_policy(self):
        # Given
        an_event = {'authorizationToken': 'a_token', 'methodArn': 'a_method'}

        # When
        auth_response: dict = handle(an_event, context={})

        # Then
        assert 'principalId' in auth_response.keys()
        assert 'policyDocument' in auth_response.keys()

    def test_authorizer_should_return_an_allowed_policy_based_on_authorization_token_value(self):
        # Given
        a_valid_event = {'authorizationToken': 'valid', 'methodArn': 'arn:aws:fakearn'}

        # When
        valid_auth_response: dict = handle(a_valid_event, context={})

        # Then
        expected_effect = 'Allow'
        assert valid_auth_response == {
            'principalId': 'hallebarde_authorizer',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'execute-api:Invoke',
                    'Effect': expected_effect,
                    'Resource': 'arn:aws:fakearn'
                }]
            }
        }

    def test_authorizer_should_return_a_denied_policy_when_authorization_token_value_is_invalid(self):
        # Given
        an_invalid_event = {'authorizationToken': 'invalid', 'methodArn': 'arn:aws:fakearn'}

        # When
        invalid_auth_response: dict = handle(an_invalid_event, context={})

        # Then
        expected_effect = 'Deny'
        assert invalid_auth_response == {
            'principalId': 'hallebarde_authorizer',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'execute-api:Invoke',
                    'Effect': expected_effect,
                    'Resource': 'arn:aws:fakearn'
                }]
            }
        }

    def test_handle_should_log_processing_event(self):
        # Given
        a_valid_event = {'authorizationToken': 'valid', 'methodArn': 'arn:aws:fakearn'}

        # When
        with self.assertLogs(level='INFO') as cm:
            handle(a_valid_event, context={})

        # Then
        expected_log = "INFO:root:Processing event {'authorizationToken': 'valid', 'methodArn': 'arn:aws:fakearn'}"
        assert expected_log in cm.output
