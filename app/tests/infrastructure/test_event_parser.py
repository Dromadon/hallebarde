from hallebarde.infrastructure import event_parser


class TestEventParser:

    def test_extract_email_should_return_email_value_from_headers(self, generic_event):
        # Given
        expected_email = generic_event['headers']['email']

        # When
        actual_email = event_parser.extract_from_headers('email', generic_event)

        # Then
        assert actual_email == expected_email

    def test_extract_identifier_should_return_identifier_value_from_headers(self, revoke_event):
        # Given
        expected_identifier = revoke_event['headers']['exchange_identifier']

        # When
        actual_identifier = event_parser.extract_from_headers('exchange_identifier', revoke_event)

        # Then
        assert actual_identifier == expected_identifier

    def test_extract_upload_token_should_return_identifier_value_from_headers(self, upload_url_event):
        # Given
        expected_token = upload_url_event['headers']['upload_token']

        # When
        actual_token = event_parser.extract_from_headers('upload_token', upload_url_event)

        # Then
        assert actual_token == expected_token

    def test_extract_filename_should_return_filename_value_from_headers(self, upload_url_event):
        # Given
        expected_filename = upload_url_event['headers']['filename']

        # When
        actual_filename = event_parser.extract_from_headers('filename', upload_url_event)

        # Then
        assert actual_filename == expected_filename
