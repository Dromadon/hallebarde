from http import HTTPStatus
from unittest import mock
from unittest.mock import patch, PropertyMock

from hallebarde.responses import endpoint_responses


class TestEndpointResponses:

    def test_generate_response_should_return_response_with_expected_fields(self):
        # Given
        body = {}
        status_code = HTTPStatus.OK

        # When
        response = endpoint_responses.generate_response(body, status_code)

        # Then
        assert response['isBase64Encoded'] is False
        assert response['headers'] == {'Access-Control-Allow-Origin': "*"}
        assert response['body'] == body
        assert response['statusCode'] == status_code

    @patch('hallebarde.responses.endpoint_responses.config')
    def test_get_allowed_origin_should_return_wildcard_when_env_is_dev(self, mock_config):
        # Given
        mock_config.ENVIRONMENT = 'dev'

        # When
        origin = endpoint_responses.get_allowed_origin()

        # Then
        assert origin == "*"

    @patch('hallebarde.responses.endpoint_responses.config')
    def test_get_allowed_origin_should_return_website_hostname_when_env_is_not_dev(self, mock_config):
        # Given
        website_hostname = 'https://ourwebsite'
        mock_config.ENVIRONMENT = 'prod'
        mock_config.WEBSITE_HOSTNAME = website_hostname

        # When
        origin = endpoint_responses.get_allowed_origin()

        # Then
        assert origin == website_hostname
