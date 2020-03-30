from unittest.mock import patch

from hallebarde.domain.exchange import Exchange
from hallebarde.revoke_exchange import handle


class TestRevokeExchange:

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.revoke_an_exchange')
    def test_handle_should_return_a_200_status(self, revoke_an_exchange, mock_exchange_repo,
                                                   revoke_event,
                                                   event_sub):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate(event_sub)

        # When
        response = handle(event=revoke_event, context={})

        # Then
        assert response['body'] == 'Exchange revoked'
        assert response['statusCode'] == 200

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.revoke_an_exchange')
    def test_handle_should_launch_a_revoke_command(self, revoke_an_exchange, mock_exchange_repo,
                                                   revoke_event,
                                                   event_sub):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate(event_sub)

        # When
        handle(event=revoke_event, context={})

        # Then
        revoke_an_exchange.revoke_an_exchange_by_its_identifier.assert_called_once_with(revoke_event['headers']['exchange_identifier'])

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.revoke_an_exchange')
    def test_handle_should_return_403_if_jwt_sub_does_not_match_exchange_sub(self, revoke_an_exchange,
                                                                             mock_exchange_repo, revoke_event,
                                                                             an_exchange):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate('a_different_sub')

        # When
        response = handle(event=revoke_event, context={})

        # Then
        assert response['body'] == 'Forbidden'
        assert response['statusCode'] == 403

