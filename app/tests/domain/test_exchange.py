from unittest import TestCase
from unittest.mock import patch

from hallebarde.domain.exchange import Exchange


class TestExchange(TestCase):

    def test_exchanges_should_be_compared_on_identifier_email_and_tokens(self):
        # Given
        exchange1 = Exchange('id1', 'email1', 'up1', 'dl1')
        exchange1bis = Exchange('id1', 'email1', 'up1', 'dl1')
        exchange2 = Exchange('id2', 'email2', 'up2', 'dl2')

        # Then
        assert exchange1 == exchange1bis
        assert exchange1 != exchange2

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
