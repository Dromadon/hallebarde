from unittest import TestCase
from unittest.mock import patch, Mock

from botocore.exceptions import ClientError

from hallebarde.get_presigned_url import handle


class TestGetPresignedUrl(TestCase):

    @patch('hallebarde.get_presigned_url.boto3')
    def test_get_presigned_url_logs_an_error_when_failing(self, mock_boto3):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceInUseException'}},
            operation_name='generate_presigned_post')
        mock_boto3.client.return_value = mock_client

        # When
        with self.assertLogs(level='ERROR') as cm:
            handle(event={}, context={})

        # Then
        assert f'ERROR:root:An error occurred (ResourceInUseException) when calling ' \
               'the generate_presigned_post operation: Unknown' \
               in cm.output

    @patch('hallebarde.get_presigned_url.boto3')
    def test_get_presigned_url_returns_a_response_containing_a_presigned_url(self, mock_boto3):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.return_value = {
            'url': 'https://mybucket.s3.amazonaws.com',
            'fields': {
                'acl': 'public-read',
                'key': 'mykey',
                'signature': 'mysignature',
                'policy': 'mybase64 encoded policy'
            }
        }
        mock_boto3.client.return_value = mock_client

        # When
        response_with_presigned_url: dict = handle(event={}, context={})

        # Then
        assert response_with_presigned_url == {
            "isBase64Encoded": False,
            "body": '{"url": "https://mybucket.s3.amazonaws.com", '
                    '"fields": {"acl": "public-read", "key": "mykey", '
                    '"signature": "mysignature", "policy": "mybase64 encoded policy"}}',
            "headers": None,
            "statusCode": 200
        }
