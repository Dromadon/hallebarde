from unittest.mock import patch, call

from hallebarde.domain.exchange import Exchange
from hallebarde.revoke_exchange import handle


class TestRevokeExpiredExchanges:

    @patch('hallebarde.revoke_exchange.exchange_repository')
    @patch('hallebarde.revoke_exchange.revoke_an_exchange')
    def test_handle_should_launch_revoke_command_for_each_expired_exchange(self, mock_revoke_an_exchange,
                                                                           mock_exchange_repo, generic_event,
                                                                           an_exchange, an_exchange_with_different_sub):
        # Given
        mock_exchange_repo.get_before_time.return_value = [an_exchange, an_exchange_with_different_sub]
        expected_args_list = [call(an_exchange.identifier), call(an_exchange_with_different_sub.identifier)]

        # When
        handle(generic_event, context={})

        # Then
        assert mock_revoke_an_exchange.revoke_an_exchange_by_its_identifier.has_calls(expected_args_list)
