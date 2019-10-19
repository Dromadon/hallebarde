from unittest import TestCase
from unittest.mock import patch

from hallebarde.get_token import handle


class TestToken(TestCase):

    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self):
        # When
        response: dict = handle(event={}, context={})

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], dict) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)

    @patch('hallebarde.get_token.generate_token')
    def test_handle_should_return_upload_and_download_token_in_its_body(self, mock_generate_token):
        # Given
        expected_upload_token = "9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y"
        expected_download_token = "2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4"
        mock_generate_token.side_effect = [expected_upload_token, expected_download_token]

        # When
        response: dict = handle(event={}, context={})

        # Then
        assert response == {
            "isBase64Encoded": False,
            "body": {
                "upload_token": expected_upload_token,
                "download_token": expected_download_token
            },
            "headers": None,
            "statusCode": 200
        }
