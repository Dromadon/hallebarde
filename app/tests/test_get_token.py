from unittest import TestCase
from unittest.mock import patch
import json

from hallebarde.domain.exchange import Exchange
from hallebarde.get_token import handle


class TestToken(TestCase):

    @patch('hallebarde.get_token.exchange_repository')
    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self, mock_token_repo):
        # When
        response: dict = handle(event={}, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], str) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.get_token.exchange_repository')
    @patch('hallebarde.get_token.generate_identifier')
    @patch('hallebarde.get_token.generate_token')
    def test_handle_should_return_upload_and_download_token_in_its_body(self, mock_generate_token,
                                                                        mock_generate_identifier, mock_token_repo):
        # Given
        expected_id = "224c74ed-eeac-47d2-b8fe-165a0e30815f"
        expected_upload_token = "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y"
        expected_download_token = "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4"
        expected_body = json.dumps({"identifier": expected_id, "upload_token": expected_upload_token,
                                    "download_token": expected_download_token})
        mock_generate_token.side_effect = [expected_upload_token, expected_download_token]
        mock_generate_identifier.return_value = expected_id

        # When
        response: dict = handle(event={}, context={})

        # Then
        assert response == {
            "isBase64Encoded": False,
            "body": expected_body,
            "headers": None,
            "statusCode": 200
        }

    @patch('hallebarde.get_token.exchange_repository')
    @patch('hallebarde.get_token.Exchange')
    def test_handle_should_create_token_in_db(self, mock_exchange, mock_token_repo):
        # Given
        expected_exchange = Exchange('224c74ed-eeac-47d2-b8fe-165a0e30815f',
                                     "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y",
                                     "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4")

        mock_exchange.return_value = expected_exchange

        # When
        handle(event={}, context={})

        # Then
        mock_token_repo.save.assert_called_once_with(expected_exchange)
