from http import HTTPStatus

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
        assert response['headers'] is None
        assert response['body'] == body
        assert response['statusCode'] == status_code
