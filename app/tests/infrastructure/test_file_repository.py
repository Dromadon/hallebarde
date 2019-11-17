from time import sleep
from unittest.mock import patch

import pytest

from hallebarde.infrastructure import file_repository
import hallebarde.config

BUCKET_NAME = f'hallebarde-storage-{hallebarde.config.ENVIRONMENT}'


@pytest.mark.usefixtures("get_s3_client")
class TestFileRepository:

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_get_file_should_return_none_if_identifier_has_no_file(self, mock_get_s3_client, get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client

        # When
        actual_file = file_repository.get_file('non-existing-identifier')

        # Then
        assert actual_file is None

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_get_file_should_return_the_exchange_file(self, mock_get_s3_client, an_exchange, get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client
        get_s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{an_exchange.identifier}/a_binary_content')

        # When
        actual_file = file_repository.get_file(an_exchange.identifier)

        # Then
        assert actual_file == f'{an_exchange.identifier}/a_binary_content'

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_get_file_should_return_only_the_exchange_file(self, mock_get_s3_client, an_exchange,
                                                           an_exchange_with_different_email, get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client
        get_s3_client.put_object(Bucket=BUCKET_NAME,
                                 Key=f'{an_exchange_with_different_email.identifier}/another_binary_content')
        get_s3_client.put_object(Bucket=BUCKET_NAME,
                                 Key=f'{an_exchange.identifier}/a_binary_content')

        # When
        actual_file = file_repository.get_file(an_exchange.identifier)

        # Then
        assert actual_file == f'{an_exchange.identifier}/a_binary_content'

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_get_file_should_return_the_last_uploaded_exchange_file(self, mock_get_s3_client, an_exchange,
                                                                    get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client
        get_s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{an_exchange.identifier}/a_binary_content')
        sleep(1)
        get_s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{an_exchange.identifier}/another_binary_content')

        # When
        actual_file = file_repository.get_file(an_exchange.identifier)

        # Then
        assert actual_file == f'{an_exchange.identifier}/another_binary_content'

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_delete_should_remove_all_files_related_to_identifier(self, mock_get_s3_client,
                                                                  an_exchange, get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client
        get_s3_client.put_object(Bucket=BUCKET_NAME,
                                 Key=f'{an_exchange.identifier}/a_binary_content')
        get_s3_client.put_object(Bucket=BUCKET_NAME,
                                 Key=f'{an_exchange.identifier}/another_binary_content')

        # When
        file_repository.delete_files(an_exchange.identifier)

        # Then
        actual_files_list = file_repository._get_files(an_exchange.identifier)
        assert actual_files_list is None

    @patch('hallebarde.infrastructure.file_repository._get_s3_client')
    def test_delete_should_do_nothing_if_identifier_does_not_exist(self, mock_get_s3_client,
                                                                   an_exchange, get_s3_client):
        # Given
        mock_get_s3_client.return_value = get_s3_client

        # When
        file_repository.delete_files('a_fake_identifier')
