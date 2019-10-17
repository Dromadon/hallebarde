import unittest
from unittest.mock import patch

from hallebarde.get_token import handle


class TestToken(unittest.TestCase):

    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self):
        # Given
        event = {}
        context = {}

        # When
        response = handle(event, context)

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], dict) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.get_token.generate_token')
    def test_handle_should_return_upload_and_download_token_in_body(self, mock_generate_token):
        # Given
        event = {}
        context = {}
        expected_upload_token = "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y"
        expected_download_token = "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4"
        mock_generate_token.side_effect = [expected_upload_token, expected_download_token]

        # When
        response = handle(event, context)

        # Then
        assert response['body']['upload_token'] == expected_upload_token
        assert response['body']['download_token'] == expected_download_token
