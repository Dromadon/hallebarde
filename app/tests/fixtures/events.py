import pytest


@pytest.fixture
def generic_event():
    return {'headers': {'email': 'me@mydomain'}}


@pytest.fixture
def revoke_event():
    return {'headers': {'exchange_identifier': '97de5cec-33e6-49ae-8ee8-8865ce357625'}}
