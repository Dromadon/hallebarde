from unittest import TestCase

from hallebarde.infrastructure import event_parser


class TestEventParser(TestCase):

    def test_extract_email_should_return_email_value_from_headers(self):
        # Given
        expected_email = 'me@mydomain'
        event = {'headers': {'email': expected_email}}

        # When
        actual_email = event_parser.extract_email_from_headers(event)

        # Then
        assert actual_email == expected_email
