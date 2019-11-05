from hallebarde.infrastructure import event_parser


class TestEventParser:

    def test_extract_email_should_return_email_value_from_headers(self, generic_event):
        # Given
        expected_email = generic_event['headers']['email']

        # When
        actual_email = event_parser.extract_email_from_headers(generic_event)

        # Then
        assert actual_email == expected_email

    def test_extract_identifier_should_return_identifier_value_from_headers(self, revoke_event):
        # Given
        expected_identifier = revoke_event['headers']['exchange_identifier']

        # When
        actual_identifier = event_parser.extract_identifier_from_headers(revoke_event)

        # Then
        assert actual_identifier == expected_identifier
