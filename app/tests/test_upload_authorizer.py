from unittest.mock import patch

from hallebarde.upload_authorizer import validate, handle


class TestAuthorizer:

    @patch('hallebarde.upload_authorizer.exchange_repository')
    def test_validate_should_return_true_if_an_exchange_exists_and_is_not_revoked(self, mock_exchange_repository,
                                                                                  an_exchange,
                                                                                  a_revoked_upload_exchange):
        # Given
        mock_exchange_repository.get_by_upload_token.side_effect = [an_exchange, a_revoked_upload_exchange]

        # When
        validation1: bool = validate(an_exchange.upload_token)
        validation2: bool = validate(a_revoked_upload_exchange.upload_token)

        # Then
        assert validation1 is True
        assert validation2 is False

    @patch('hallebarde.upload_authorizer.exchange_repository')
    def test_validate_should_return_false_if_no_exchange_returned_from_repository(self, mock_exchange_repository,
                                                                                  an_exchange):
        # Given
        mock_exchange_repository.get_by_upload_token.return_value = None

        # When
        validation: bool = validate(an_exchange.upload_token)

        # Then
        assert validation is False

    @patch('hallebarde.upload_authorizer.validate')
    @patch('hallebarde.responses.authorizer_responses.generate_aws_policy')
    def test_authorizer_should_return_an_allowed_policy_based_on_authorization_token_value(self, mock_generate_policy,
                                                                                           mock_validate,
                                                                                           authorizer_event):
        # Given
        mock_validate.return_value = True

        # When
        handle(authorizer_event, context={})

        # Then
        mock_generate_policy.assert_called_once_with(True, authorizer_event['methodArn'])

    @patch('hallebarde.upload_authorizer.validate')
    @patch('hallebarde.responses.authorizer_responses.generate_aws_policy')
    def test_authorizer_should_return_a_denied_policy_when_authorization_token_value_is_invalid(self,
                                                                                                mock_generate_policy,
                                                                                                mock_validate,
                                                                                                authorizer_event):
        # Given
        mock_validate.return_value = False

        # When
        handle(authorizer_event, context={})

        # Then
        mock_generate_policy.assert_called_once_with(False, authorizer_event['methodArn'])
