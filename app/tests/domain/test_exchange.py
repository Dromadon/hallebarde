from unittest import TestCase
from unittest.mock import patch

from hallebarde.domain.exchange import Exchange

from datetime import datetime, timezone


class TestExchange(TestCase):

    def test_an_exchange_should_be_created_with_revoked_upload_set_to_false(self):
        # Given
        exchange = Exchange('id1', 'sub1', 'up1', 'dl1')

        # Then
        assert exchange.revoked_upload is False

    def test_exchanges_should_be_compared_on_identifier_email_tokens_upload_revocation_and_creation_time(self):
        # Given
        exchange1 = Exchange(identifier='id1', sub='sub1', upload_token='up1', download_token='dl1',
                             revoked_upload=False, creation_time=datetime.now())
        exchange1bis = Exchange('id1', 'sub1', 'up1', 'dl1', False, exchange1.creation_time)
        exchange2 = Exchange('id2', 'sub2', 'up2', 'dl2', False, exchange1.creation_time)
        exchange3 = Exchange('id1', 'sub1', 'up1', 'dl1', True, exchange1.creation_time)
        exchange4 = Exchange('id1', 'sub1', 'up1', 'dl1', False, datetime(2000,1,1))

        # Then
        assert exchange1 == exchange1bis
        assert exchange1 != exchange2
        assert exchange1 != exchange3
        assert exchange1 != exchange4

    @patch('hallebarde.domain.exchange.uuid4')
    @patch('hallebarde.domain.exchange.token_urlsafe')
    def test_an_exchange_can_be_generated_automatically(self, mock_token, mock_uuid):
        # Given
        mock_uuid.return_value = 'id1'
        mock_token.side_effect = ['up1', 'dl1']

        # When
        generated_exchange = Exchange.generate('sub1')

        # Then
        expected_exchange = Exchange('id1', 'sub1', 'up1', 'dl1', False, generated_exchange.creation_time)
        assert expected_exchange == generated_exchange
        assert expected_exchange.creation_time < datetime.now(timezone.utc)