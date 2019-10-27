from unittest import TestCase
from unittest.mock import patch

from hallebarde.domain.exchange import Exchange
from hallebarde.get_exchange import handle


class TestExchange(TestCase):

    @patch('hallebarde.get_exchange.exchange_repository')
    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self, mock_exchange_repo):
        # Given
        mock_exchange_repo.save.return_value = None

        # When
        response: dict = handle(event={}, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], str) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.get_exchange.exchange_repository')
    @patch('hallebarde.get_exchange.Exchange')
    def test_handle_should_return_upload_and_download_token_in_its_body(self, mock_exchange,
                                                                        mock_exchange_repo):
        # Given
        mock_exchange_repo.save.return_value = None
        mock_exchange.generate.return_value = Exchange(
            identifier="224c74ed-eeac-47d2-b8fe-165a0e30815f",
            upload_token="9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y",
            download_token="2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4")

        # When
        response: dict = handle(event={}, context={})

        # Then
        assert response == {
            "isBase64Encoded": False,
            "body": '{"identifier": "224c74ed-eeac-47d2-b8fe-165a0e30815f", '
                    '"upload_token": "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y", '
                    '"download_token": "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4"}',
            "headers": None,
            "statusCode": 200
        }

    @patch('hallebarde.get_exchange.exchange_repository')
    @patch('hallebarde.get_exchange.Exchange')
    def test_handle_should_create_token_in_db(self, mock_exchange, mock_exchange_repo):
        # Given
        expected_exchange = Exchange('224c74ed-eeac-47d2-b8fe-165a0e30815f',
                                     "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y",
                                     "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4")

        mock_exchange.generate.return_value = expected_exchange

        # When
        handle(event={}, context={})

        # Then
        mock_exchange_repo.save.assert_called_once_with(expected_exchange)
