from unittest import TestCase

from hallebarde.domain.exchange import Exchange


class TestExchange(TestCase):

    def test_exchanges_should_be_compared_on_identifier_and_tokens(self):
        # Given
        exchange1 = Exchange('id1', 'up1', 'dl1')
        exchange1bis = Exchange('id1', 'up1', 'dl1')
        exchange2 = Exchange('id2', 'up2', 'dl2')

        # Then
        assert exchange1 == exchange1bis
        assert exchange1 != exchange2
