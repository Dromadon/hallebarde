import json
from unittest.mock import patch

from hallebarde.get_account_exchanges import handle


class TestToken:

    @patch('hallebarde.get_account_exchanges.exchange_repository')
    def test_handle_should_return_exchanges_given_by_repository(self, mock_exchange_repo, generic_event,
                                                                two_exchanges_with_same_sub):
        # Given
        mock_exchange_repo.get_account_exchanges.return_value = two_exchanges_with_same_sub

        # When
        response: dict = handle(generic_event, context={})

        # Then
        assert response['body'] == json.dumps(
            [two_exchanges_with_same_sub[0].__dict__, two_exchanges_with_same_sub[1].__dict__], default=str)
        assert response['statusCode'] == 200

    @patch('hallebarde.get_account_exchanges.exchange_repository')
    def test_handle_should_extract_email_from_headers(self, mock_exchange_repo, generic_event, event_sub):
        # Given

        # When
        handle(event=generic_event, context={})

        # Then
        mock_exchange_repo.get_account_exchanges.assert_called_once_with(event_sub)
