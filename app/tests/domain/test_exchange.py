from unittest import TestCase
from unittest.mock import patch

from hallebarde.domain.exchange import Exchange


class TestExchange(TestCase):

    def test_an_exchange_should_be_created_with_revoked_upload_set_to_false(self):
        # Given
        exchange = Exchange('id1', 'email1', 'up1', 'dl1')

        # Then
        assert exchange.revoked_upload is False

    def test_exchanges_should_be_compared_on_identifier_email_tokens_and_revocation(self):
        # Given
        exchange1 = Exchange(identifier='id1', email='email1', upload_token='up1', download_token='dl1',
                             revoked_upload=False)
        exchange1bis = Exchange('id1', 'email1', 'up1', 'dl1')
        exchange2 = Exchange('id2', 'email2', 'up2', 'dl2')
        exchange3 = Exchange('id1', 'email1', 'up1', 'dl1', True)

        # Then
        assert exchange1 == exchange1bis
        assert exchange1 != exchange2
        assert exchange1 != exchange3

    @patch('hallebarde.domain.exchange.uuid4')
    @patch('hallebarde.domain.exchange.token_urlsafe')
    def test_an_exchange_can_be_generated_automatically(self, mock_token, mock_uuid):
        # Given
        mock_uuid.return_value = 'id1'
        mock_token.side_effect = ['up1', 'dl1']

        # When
        generated_exchange = Exchange.generate('email@none')

        # Then
        expected_exchange = Exchange('id1', 'email@none', 'up1', 'dl1')
        assert expected_exchange == generated_exchange
