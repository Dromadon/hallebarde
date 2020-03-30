from unittest.mock import patch

from hallebarde.usecases import revoke_an_exchange


class TestRevokeExchange:

    @patch('hallebarde.usecases.revoke_an_exchange.exchange_repository')
    @patch('hallebarde.usecases.revoke_an_exchange.file_repository')
    def test_handle_should_delete_exchange_in_db(self, mock_file_repository, mock_exchange_repo):
        # Given

        # When
        revoke_an_exchange.revoke_an_exchange_by_its_identifier(identifier='test_identifier')

        # Then
        mock_exchange_repo.delete.assert_called_once_with('test_identifier')

    @patch('hallebarde.usecases.revoke_an_exchange.exchange_repository')
    @patch('hallebarde.usecases.revoke_an_exchange.file_repository')
    def test_handle_should_delete_files_associated_with_exchange(self, mock_file_repository, mock_exchange_repo):
        # Given
        identifier = 'test_identifier'

        # When
        revoke_an_exchange.revoke_an_exchange_by_its_identifier(identifier)

        # Then
        mock_file_repository.delete_files.assert_called_once_with(identifier)
