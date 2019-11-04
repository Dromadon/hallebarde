import json
from unittest.mock import patch

from hallebarde.create_exchange import handle


class TestExchange:

    @patch('hallebarde.create_exchange.exchange_repository')
    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self, mock_exchange_repo, generic_event):
        # Given
        mock_exchange_repo.save.return_value = None

        # When
        response: dict = handle(event=generic_event, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], str) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)

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
        assert response == {
            "isBase64Encoded": False,
            "body": json.dumps(an_exchange.__dict__),
            "headers": None,
            "statusCode": 200
        }

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
    def test_handle_should_use_email_provided_in_headers(self, mock_exchange_generate, mock_exchange_repo,
                                                         generic_event, an_exchange):
        # Given
        mock_exchange_generate.return_value = an_exchange

        # When
        handle(event=generic_event, context={})

        # Then
        mock_exchange_generate.assert_called_once_with(generic_event['headers']['email'])
