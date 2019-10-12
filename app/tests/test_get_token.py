from hallebarde.get_token import handle

class TestToken:


    def test_handle_should_return_a_correctly_formed_lambda_proxy_response(self):
        # Given
        event = {}
        context = {}

        # When
        response = handle(event, context)

        # Then
        assert isinstance(response['isBase64Encoded'], bool)
        assert isinstance(response['body'], dict) or response['body'] is None
        assert isinstance(response['headers'], dict) or response['headers'] is None
        assert isinstance(response['statusCode'], int)