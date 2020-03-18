from hallebarde.responses.authorizer_responses import generate_aws_policy, generate_response


class TestAuthorizerResponses:

    def test_generate_policy_should_return_a_policy_containing_a_version_and_a_statement(self):
        # When
        policy: dict = generate_aws_policy(is_valid=True, resource='a_resource')

        # Then
        assert 'Version' in policy.keys()
        assert 'Statement' in policy.keys()

    def test_generate_policy_should_return_an_allowed_policy_on_given_resource(self):
        # Given
        policy_validity = True

        # When
        policy: dict = generate_aws_policy(policy_validity, 'arn:aws:fakearn')

        # Then
        assert policy == {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': 'arn:aws:fakearn'
            }]
        }

    def test_generate_policy_should_return_a_denied_policy_on_a_resource_when_invalid(self):
        # Given
        policy_validity = False

        # When
        policy: dict = generate_aws_policy(policy_validity, 'arn:aws:fakearn')

        # Then
        assert policy == {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Deny',
                'Resource': 'arn:aws:fakearn'
            }]
        }

    def test_authorizer_should_return_an_authentication_with_an_id_and_a_policy(self):
        # When
        auth_response: dict = generate_response("aprincipalid", {})

        # Then
        assert 'principalId' in auth_response.keys()
        assert 'policyDocument' in auth_response.keys()
