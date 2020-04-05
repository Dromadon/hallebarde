from datetime import datetime, timezone, timedelta
from unittest.mock import patch

import pytest

from hallebarde.infrastructure import exchange_repository

TABLE_NAME = f'hallebarde-dev-table'


@pytest.mark.usefixtures("setup_dynamodb_container")
@pytest.mark.usefixtures("get_dynamodb_table")
class TestExchangeRepositoryBasics:

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_save_should_create_readable_item(self, mock_get_table, an_exchange, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        exchange_repository.save(an_exchange)

        # Then
        actual_exchange = exchange_repository.get(an_exchange.identifier)
        assert actual_exchange == an_exchange

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_should_return_none_if_no_id_is_matched(self, mock_get_table, an_exchange, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        exchange_repository.save(an_exchange)

        # Then
        actual_exchange = exchange_repository.get('non-existent-id')
        assert actual_exchange is None

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_account_exchanges_should_return_only_account_exchanges(self, mock_get_table,
                                                                        two_exchanges_with_same_sub,
                                                                        an_exchange_with_different_sub,
                                                                        get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        for exchange in two_exchanges_with_same_sub:
            exchange_repository.save(exchange)
        exchange_repository.save(an_exchange_with_different_sub)

        # When
        actual_exchanges = exchange_repository.get_account_exchanges(two_exchanges_with_same_sub[0].sub)

        # Then
        assert actual_exchanges[0] in two_exchanges_with_same_sub
        assert actual_exchanges[1] in two_exchanges_with_same_sub
        assert len(actual_exchanges) == 2

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_delete_should_delete_indicated_exchange(self, mock_get_table, an_exchange, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        exchange_repository.save(an_exchange)

        # When
        exchange_repository.delete(an_exchange.identifier)

        # Then
        assert exchange_repository.get(an_exchange.identifier) is None


@pytest.mark.usefixtures("setup_dynamodb_container")
@pytest.mark.usefixtures("get_dynamodb_table")
class TestExchangeRepositoryGettingByToken:
    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_identifier_from_token_should_return_identifier_associated_with_given_token(self, mock_get_table,
                                                                                            an_exchange,
                                                                                            get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        exchange_repository.save(an_exchange)

        # When
        identifier_from_upload_token = exchange_repository.get_identifier_from_token(
            upload_token=an_exchange.upload_token)
        identifier_from_download_token = exchange_repository.get_identifier_from_token(
            download_token=an_exchange.download_token)

        # Then
        assert identifier_from_upload_token == an_exchange.identifier
        assert identifier_from_download_token == an_exchange.identifier

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_identifier_from_token_should_return_none_if_exchange_does_not_exist(self, mock_get_table,
                                                                                     an_exchange,
                                                                                     get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        identifier_from_upload_token = exchange_repository.get_identifier_from_token(upload_token="fake_upload_token")
        identifier_from_download_token = exchange_repository.get_identifier_from_token(
            download_token="fake_download_token")

        # Then
        assert identifier_from_upload_token is None
        assert identifier_from_download_token is None

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_identifier_from_token_should_be_none_safe(self, mock_get_table, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        identifier_from_upload_token = exchange_repository.get_identifier_from_token()

        # Then
        assert identifier_from_upload_token is None

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_revoke_upload_token(self, mock_get_table, an_exchange, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        exchange_repository.save(an_exchange)

        # When
        exchange_repository.revoke_upload(an_exchange.identifier)
        actual_exchange = exchange_repository.get(an_exchange.identifier)

        # Then
        assert actual_exchange.revoked_upload is True

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_by_upload_token_should_return_exchange(self, mock_get_table, get_dynamodb_table, an_exchange):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        exchange_repository.save(an_exchange)

        # When
        actual_exchange = exchange_repository.get_by_upload_token(an_exchange.upload_token)

        # Then
        assert actual_exchange == an_exchange

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_by_upload_token_should_return_none_if_no_exchange_exists(self, mock_get_table, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        actual_exchange = exchange_repository.get_by_upload_token('anonexistingexchange')

        # Then
        assert actual_exchange is None

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_by_download_token_should_return_an_exchange(self, mock_get_table, get_dynamodb_table, an_exchange):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        exchange_repository.save(an_exchange)

        # When
        actual_exchange = exchange_repository.get_by_download_token(an_exchange.download_token)

        # Then
        assert actual_exchange == an_exchange

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_by_download_token_should_return_none_if_no_exchange_exists(self, mock_get_table, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        actual_exchange = exchange_repository.get_by_download_token('anonexistingexchange')

        # Then
        assert actual_exchange is None


@pytest.mark.usefixtures("setup_dynamodb_container")
@pytest.mark.usefixtures("get_dynamodb_table")
class TestExchangeRepositoryActionsBasedOnTime:
    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_before_time_should_return_empty_list_if_no_exchanges_exist_before_this_time(self,
                                                                                                        mock_get_table,
                                                                                                        get_dynamodb_table,
                                                                                                        generate_old_exchange):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        week_before = datetime.now(timezone.utc) - timedelta(days=7)

        # When
        actual_exchanges = exchange_repository.get_before_time(week_before)

        # Then
        assert actual_exchanges == []

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_get_before_time_should_return_only_exchanges_created_before_this_time(self, mock_get_table,
                                                                                   get_dynamodb_table, an_exchange,
                                                                                   generate_old_exchange):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        time_before = datetime.now(timezone.utc) - timedelta(days=2)

        old_exchange = generate_old_exchange(days_before=3)
        exchange_repository.save(an_exchange)
        exchange_repository.save(old_exchange)

        # When
        actual_exchanges = exchange_repository.get_before_time(time_before)

        # Then
        assert actual_exchanges == [old_exchange]


