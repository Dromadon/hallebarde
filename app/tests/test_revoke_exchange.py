from unittest.mock import patch

from hallebarde.domain.exchange import Exchange
from hallebarde.revoke_exchange import handle


class TestRevokeExchange:

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.file_repository')
    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self, mock_file_repository,
                                                                           mock_exchange_repo, revoke_event, event_sub):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate(event_sub)

        # When
        response: dict = handle(event=revoke_event, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert response['body'] == "Exchange revoked"
        assert response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.file_repository')
    def test_handle_should_delete_exchange_in_db(self, mock_file_repository, mock_exchange_repo, revoke_event,
                                                 event_sub):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate(event_sub)

        # When
        handle(event=revoke_event, context={})

        # Then
        mock_exchange_repo.delete.assert_called_once_with(revoke_event['headers']['exchange_identifier'])

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.file_repository')
    def test_handle_should_delete_files_associated_with_exchange(self, mock_file_repository, mock_exchange_repo,
                                                                 revoke_event, event_sub):
        # Given
        called_identifier = revoke_event['headers']['exchange_identifier']
        mock_exchange_repo.get.return_value = Exchange.generate(event_sub)

        # When
        handle(event=revoke_event, context={})

        # Then
        mock_file_repository.delete_files.assert_called_once_with(called_identifier)

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.file_repository')
    def test_handle_should_return_403_if_jwt_sub_does_not_match_exchange_sub(self, mock_file_repository,
                                                                             mock_exchange_repo, revoke_event,
                                                                             an_exchange):
        # Given
        mock_exchange_repo.get.return_value = Exchange.generate('a_different_sub')

        # When
        response = handle(event=revoke_event, context={})

        # Then
        assert response == {
            "isBase64Encoded": False,
            "body": "Forbidden",
            "headers": None,
            "statusCode": 403
        }
