from unittest.mock import patch

from hallebarde.revoke_exchange import handle


class TestRevokeExchange:

    @patch('hallebarde.revoke_exchange.exchange_repository')
    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self, mock_exchange_repo, revoke_event):
        # When
        response: dict = handle(event=revoke_event, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert response['body'] is None
        assert response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.revoke_exchange.exchange_repository')
    def test_handle_should_delete_exchange_in_db(self, mock_exchange_repo, revoke_event):
        # When
        handle(event=revoke_event, context={})

        # Then
        mock_exchange_repo.delete.assert_called_once_with(revoke_event['headers']['exchange_identifier'])
