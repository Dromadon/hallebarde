import json
from unittest.mock import patch, Mock

from botocore.exceptions import ClientError

import hallebarde.config
from hallebarde.get_presigned_upload_url import handle


class TestGetUploadPresignedUrl:
    BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'

    @patch('hallebarde.get_presigned_upload_url.boto3')
    @patch('hallebarde.get_presigned_upload_url.exchange_repository')
    @patch('hallebarde.get_presigned_upload_url._check_if_a_file_exists')
    def test_get_presigned_post_returns_a_response_containing_a_presigned_url(self, mock_file_exists,
                                                                              mock_exchange_repository, mock_boto3,
                                                                              upload_url_event, an_exchange):
        # Given
        mock_client = Mock()
        presigned_url = {
            'url': 'https://mybucket.s3.amazonaws.com',
            'fields': {
                'acl': 'public-read',
                'key': 'mykey',
                'signature': 'mysignature',
                'policy': 'mybase64 encoded policy'
            }
        }
        mock_client.generate_presigned_post.return_value = presigned_url
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier
        mock_file_exists.return_value = False

        # When
        response_with_presigned_url: dict = handle(event=upload_url_event, context={})

        # Then
        assert response_with_presigned_url['body'] == json.dumps(presigned_url)
        assert response_with_presigned_url['statusCode'] == 200


    @patch('hallebarde.get_presigned_upload_url.boto3')
    @patch('hallebarde.get_presigned_upload_url.exchange_repository')
    @patch('hallebarde.get_presigned_upload_url._check_if_a_file_exists')
    def test_get_presigned_upload_url_should_generate_url_with_bucket_name_and_filename_key(self,
                                                                                            mock_file_exists,
                                                                                            mock_exchange_repository,
                                                                                            mock_boto3,
                                                                                            upload_url_event,
                                                                                            an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.return_value = {}
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier
        expected_filename = f'{an_exchange.identifier}/{upload_url_event["headers"]["filename"]}'

        mock_file_exists.return_value = False

        # When
        handle(event=upload_url_event, context={})
        called_args = mock_client.generate_presigned_post.call_args[0]

        # Then
        assert called_args == (self.BUCKET_NAME, expected_filename)

    @patch('hallebarde.get_presigned_upload_url.boto3')
    @patch('hallebarde.get_presigned_upload_url.exchange_repository')
    @patch('hallebarde.get_presigned_upload_url.file_repository')
    def test_get_presigned_upload_url_should_return_409_error_if_file_already_exists_for_identifier(self,
                                                                                                    mock_file_repository,
                                                                                                    mock_exchange_repository,
                                                                                                    mock_boto3,
                                                                                                    upload_url_event,
                                                                                                    an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.return_value = {}
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier
        mock_file_repository.get_file.return_value = f'{an_exchange.identifier}/already_existing_file'

        # When
        response = handle(event=upload_url_event, context={})

        # Then
        assert response["body"] == 'A file already exists for this identifier'
        assert response["statusCode"] == 409

    @patch('hallebarde.get_presigned_upload_url.boto3')
    @patch('hallebarde.get_presigned_upload_url.exchange_repository')
    @patch('hallebarde.get_presigned_upload_url._check_if_a_file_exists')
    def test_get_presigned_upload_url_should_return_500_error_if_exception_raises_in_boto(self,
                                                                                          mock_file_exists,
                                                                                          mock_exchange_repository,
                                                                                          mock_boto3,
                                                                                          upload_url_event,
                                                                                          an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceInUseException'}},
            operation_name='generate_presigned_post')
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier
        mock_file_exists.return_value = False

        # When
        response = handle(event=upload_url_event, context={})

        # Then
        assert response["body"] == 'Internal error'
        assert response["statusCode"] == 500

    @patch('hallebarde.get_presigned_upload_url.boto3')
    @patch('hallebarde.get_presigned_upload_url.exchange_repository')
    @patch('hallebarde.get_presigned_upload_url._check_if_a_file_exists')
    def test_upload_token_is_revoked_once_presigned_post_url_has_been_generated(self, mock_file_exists,
                                                                                mock_exchange_repository, mock_boto3,
                                                                                upload_url_event, an_exchange):
        # Given
        mock_client = Mock()
        mock_client.generate_presigned_post.return_value = {}
        mock_boto3.client.return_value = mock_client

        mock_exchange_repository.get_identifier_from_token.return_value = an_exchange.identifier
        mock_file_exists.return_value = False

        # When
        handle(event=upload_url_event, context={})

        # Then
        mock_exchange_repository.revoke_upload.assert_called_once_with(an_exchange.identifier)
