from hallebarde.authorizer import validate, generate_policy, handle

class TestAuthorizer:

    def test_validate_should_return_true_if_token_contains_valid(self):
        # When
        response = validate('valid')

        # Then
        assert response == True

    def test_validate_should_return_false_if_token_does_not_contain_valid(self):
        # When
        response = validate('notvalid')

        # Then
        assert response == False

    def test_generate_policy_should_return_a_dict_with_mandatory_keys(self):
        # When
        policy = generate_policy(True, 'arn:aws:fakearn')

        # Then
        assert 'Version' in policy
        assert 'Statement' in policy
        assert len(policy['Statement']) == 1
        assert 'Effect' in policy['Statement'][0]
        assert policy['Statement'][0]['Resource'] == 'arn:aws:fakearn'
        assert 'Action' in policy['Statement'][0]
        assert 'Resource' in policy['Statement'][0]

    def test_generate_policy_should_return_an_effect_with_isvalid_nature(self):
        # When
        policy_true = generate_policy(True, 'arn:aws:fakearn')
        policy_false = generate_policy(False, 'arn:aws:fakearn')

        # Then
        assert policy_true['Statement'][0]['Effect'] == 'Allow'
        assert policy_false['Statement'][0]['Effect'] == 'Deny'

    def test_authorizer_should_return_a_valid_auth_response_object(self):
        # Given
        context = {}
        event = {'authorizationToken': 'invalid', 'methodArn': 'arn:aws:fakearn'}

        # When
        auth_response = handle(event, context)

        # Then
        assert 'principalId' in auth_response
        assert 'policyDocument' in auth_response

    def test_authorizer_should_return_policy_generated_based_on_authorization_token_value(self):
        # Given
        context = {}
        event_valid = {'authorizationToken': 'valid', 'methodArn': 'arn:aws:fakearn'}
        event_invalid = {'authorizationToken': 'invalid', 'methodArn': 'arn:aws:fakearn'}

        # When
        auth_response_valid = handle(event_valid, context)
        auth_response_invalid = handle(event_invalid, context)

        # Then
        assert auth_response_valid['policyDocument']['Statement'][0]['Effect'] == 'Allow'
        assert auth_response_invalid['policyDocument']['Statement'][0]['Effect'] == 'Deny'
