from unittest.mock import patch

import pytest

from hallebarde.infrastructure import exchange_repository

TABLE_NAME = f'hallebarde-dev-table'


@pytest.mark.usefixtures("get_dynamodb_table")
class TestExchangeRepository:

    @patch('hallebarde.infrastructure.exchange_repository._get_dynamodb_table')
    def test_save_should_create_readable_item(self, mock_get_table, an_exchange, get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table

        # When
        exchange_repository.save(an_exchange)

        # Then
        actual_exchange = exchange_repository.get('e68faee7-753e-49a6-a372-dc1cdc0dae03')
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
                                                                        two_exchanges_with_same_email,
                                                                        an_exchange_with_different_email,
                                                                        get_dynamodb_table):
        # Given
        mock_get_table.return_value = get_dynamodb_table
        for exchange in two_exchanges_with_same_email:
            exchange_repository.save(exchange)
        exchange_repository.save(an_exchange_with_different_email)

        # When
        actual_exchanges = exchange_repository.get_account_exchanges(two_exchanges_with_same_email[0].email)

        # Then
        assert actual_exchanges[0] in two_exchanges_with_same_email
        assert actual_exchanges[1] in two_exchanges_with_same_email
        assert len(actual_exchanges) == 2
