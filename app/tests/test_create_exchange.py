import json
from unittest.mock import patch

from hallebarde.create_exchange import handle


class TestExchange:

    @patch('hallebarde.create_exchange.exchange_repository')
    @patch('hallebarde.create_exchange.Exchange')
    def test_handle_should_return_upload_and_download_token_in_its_body(self, mock_exchange,
                                                                        mock_exchange_repo, generic_event,
                                                                        an_exchange):
        # Given
        mock_exchange.generate.return_value = an_exchange

        # When
        response: dict = handle(event=generic_event, context={})

        # Then
        assert response["body"] == json.dumps(an_exchange.__dict__, default=str)
        assert response["statusCode"] == 200

    @patch('hallebarde.create_exchange.exchange_repository')
    @patch('hallebarde.create_exchange.Exchange')
    def test_handle_should_create_token_in_db(self, mock_exchange, mock_exchange_repo, generic_event, an_exchange):
        # Given

        mock_exchange.generate.return_value = an_exchange

        # When
        handle(event=generic_event, context={})

        # Then
        mock_exchange_repo.save.assert_called_once_with(an_exchange)

    @patch('hallebarde.create_exchange.exchange_repository')
    @patch('hallebarde.create_exchange.Exchange.generate')
    def test_handle_should_use_sub_provided_in_authorization_headers(self, mock_exchange_generate, mock_exchange_repo,
                                                                     generic_event, event_sub, an_exchange):
        # Given
        mock_exchange_generate.return_value = an_exchange

        # When
        handle(event=generic_event, context={})

        # Then
        mock_exchange_generate.assert_called_once_with(event_sub)
