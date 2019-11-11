from hallebarde.infrastructure import event_parser


class TestEventParser:

    def test_extract_jwt_should_return_jwt_token_from_headers(self, generic_event):
        # Given
        expected_email = generic_event['headers']['Authorization']

        # When
        actual_email = event_parser.extract_from_headers('Authorization', generic_event)

        # Then
        assert actual_email == expected_email

    def test_extract_header_should_return_value_from_headers(self, revoke_event):
        # Given
        expected_identifier = revoke_event['headers']['exchange_identifier']

        # When
        actual_identifier = event_parser.extract_from_headers('exchange_identifier', revoke_event)

        # Then
        assert actual_identifier == expected_identifier

    def test_extract_sub_should_return_sub_from_encoded_jwt_token(self, generic_event, event_sub):
        # Given
        expected_sub = event_sub

        # When
        actual_sub = event_parser.extract_sub_from_jwt(generic_event['headers']['Authorization'])

        # Then
        assert actual_sub == expected_sub
