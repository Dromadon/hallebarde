import pytest


@pytest.fixture
def generic_event():
    return {'headers': {'email': 'me@mydomain'}}


@pytest.fixture
def revoke_event():
    return {'headers': {'exchange_identifier': '97de5cec-33e6-49ae-8ee8-8865ce357625'}}


@pytest.fixture
def upload_url_event():
    return {'headers': {'upload_token': '9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y', 'filename': 'a_filename'}}


@pytest.fixture
def download_url_event():
    return {'headers': {'download_token': '2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4'}}
