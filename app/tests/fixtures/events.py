import pytest


@pytest.fixture
def generic_event():
    return {'headers': {'email': 'me@mydomain'}}
