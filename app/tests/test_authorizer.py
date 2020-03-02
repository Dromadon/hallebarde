from unittest.mock import patch

from hallebarde.authorizer import validate, generate_policy, handle


class TestAuthorizer:

    @patch('hallebarde.authorizer.exchange_repository')
    def test_validate_should_return_true_if_an_exchange_exists_and_is_not_revoked(self, mock_exchange_repository,
                                                                                  an_exchange, a_revoked_exchange):
        # Given
        mock_exchange_repository.get_by_upload_token.side_effect = [an_exchange, a_revoked_exchange]

        # When
        validation1: bool = validate(an_exchange.upload_token)
        validation2: bool = validate(a_revoked_exchange.upload_token)

        # Then
        assert validation1 is True
        assert validation2 is False

    @patch('hallebarde.authorizer.exchange_repository')
    def test_validate_should_return_false_if_no_exchange_returned_from_repository(self, mock_exchange_repository,
                                                                                  an_exchange):
        # Given
        mock_exchange_repository.get_by_upload_token.side_effect = None

        # When
        validation: bool = validate(an_exchange.upload_token)

        # Then
        assert validation is False

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

    @patch('hallebarde.authorizer.validate')
    def test_authorizer_should_return_an_authentication_with_an_id_and_a_policy(self, mock_validate, authorizer_event):
        # When
        auth_response: dict = handle(authorizer_event, context={})

        # Then
        assert 'principalId' in auth_response.keys()
        assert 'policyDocument' in auth_response.keys()

    @patch('hallebarde.authorizer.validate')
    def test_authorizer_should_return_an_allowed_policy_based_on_authorization_token_value(self, mock_validate,
                                                                                           authorizer_event):
        # Given
        mock_validate.return_value = True

        # When
        valid_auth_response: dict = handle(authorizer_event, context={})

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

    @patch('hallebarde.authorizer.validate')
    def test_authorizer_should_return_a_denied_policy_when_authorization_token_value_is_invalid(self, mock_validate,
                                                                                                authorizer_event):
        # Given
        mock_validate.return_value = False

        # When
        invalid_auth_response: dict = handle(authorizer_event, context={})

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
