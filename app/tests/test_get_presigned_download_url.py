from unittest.mock import patch, Mock

from botocore.exceptions import ClientError

from hallebarde.get_presigned_download_url import handle
import hallebarde.config


class TestGetDownloadPresignedUrl:
    BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'
    PRESIGNED_URL = 'https://hallebarde-storage-dev.s3.amazonaws.com/test?AWSAccessKeyId=AKEY&Signature=ASign&x-amz-security-token=Atoken&Expires=1581887681'

    @patch('hallebarde.get_presigned_download_url.boto3')
    @patch('hallebarde.get_presigned_download_url.exchange_repository')
    @patch('hallebarde.get_presigned_download_url.file_repository')
    def test_get_presigned_download_returns_a_response_containing_a_presigned_url(self, mock_file_repository,
                                                                                  mock_exchange_repository,
                                                                                  mock_boto3,
                                                                                  download_url_event, an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = self.PRESIGNED_URL
        mock_boto3.client.return_value = mock_client

        # When
        response_with_presigned_url: dict = handle(event=download_url_event, context={})

        # Then
        assert response_with_presigned_url == {
            "isBase64Encoded": False,
            "body": self.PRESIGNED_URL,
            "headers": None,
            "statusCode": 200
        }

    @patch('hallebarde.get_presigned_download_url.boto3')
    @patch('hallebarde.get_presigned_download_url.exchange_repository')
    @patch('hallebarde.get_presigned_download_url.file_repository')
    def test_get_presigned_upload_url_should_generate_url_with_bucket_name_and_filename_key(self,
                                                                                            mock_file_repository,
                                                                                            mock_exchange_repository,
                                                                                            mock_boto3,
                                                                                            download_url_event,
                                                                                            an_exchange):
        # Given
        expected_filekey = f'{an_exchange.identifier}/a_file_name'
        expected_params = {'Bucket': self.BUCKET_NAME, 'Key': expected_filekey}

        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = self.PRESIGNED_URL
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier

        mock_file_repository.get_file.return_value = expected_filekey

        # When
        handle(event=download_url_event, context={})

        # Then
        mock_client.generate_presigned_url.assert_called_once_with('get_object', Params=expected_params)

    @patch('hallebarde.get_presigned_download_url.boto3')
    @patch('hallebarde.get_presigned_download_url.exchange_repository')
    @patch('hallebarde.get_presigned_download_url.file_repository')
    def test_get_presigned_download_should_return_a_404_error_if_no_file_exists(self, mock_file_repository,
                                                                                mock_exchange_repository,
                                                                                mock_boto3,
                                                                                download_url_event, an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_url.return_value = self.PRESIGNED_URL
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier

        mock_file_repository.get_file.return_value = None

        # When
        response_with_presigned_url: dict = handle(event=download_url_event, context={})

        # Then
        assert response_with_presigned_url == {
            "isBase64Encoded": False,
            "body": "No file associated to this token",
            "headers": None,
            "statusCode": 404
        }

    @patch('hallebarde.get_presigned_download_url.boto3')
    @patch('hallebarde.get_presigned_download_url.exchange_repository')
    @patch('hallebarde.get_presigned_download_url.file_repository')
    def test_get_presigned_download_should_return_a_500_error_if_exception_raises_in_boto(self, mock_file_repository,
                                                                                mock_exchange_repository,
                                                                                mock_boto3,
                                                                                download_url_event, an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_url.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceInUseException'}},
            operation_name='generate_presigned_url')
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier

        # When
        response_with_presigned_url: dict = handle(event=download_url_event, context={})

        # Then
        assert response_with_presigned_url == {
            "isBase64Encoded": False,
            "body": "Internal Error",
            "headers": None,
            "statusCode": 500
        }
