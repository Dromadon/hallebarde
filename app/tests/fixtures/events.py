import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

EVENT_SUB: str = "3dh310ble5s1i8uhleoap3489g"


@pytest.fixture
def generic_event():
    return {'headers': {'Authorization': generate_jwt_token()}}


@pytest.fixture
def event_sub():
    return EVENT_SUB


@pytest.fixture
def revoke_event():
    return {'headers': {'Authorization': generate_jwt_token(),
                        'exchange_identifier': '97de5cec-33e6-49ae-8ee8-8865ce357625'}}


@pytest.fixture
def upload_url_event():
    return {'headers': {'Authorization': '9WsE02XcMAekmjKHoj9Zq7_uVqc8dVz1Fq8czbZOq_Y', 'filename': 'a_filename'}}


@pytest.fixture
def download_url_event():
    return {'headers': {'Authorization': '2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4'}}


@pytest.fixture
def authorizer_event():
    return {'authorizationToken': '2yOdhL1NM5lyX7Mt8pHVYfkE51UkoSuGUrv6z4OT-c4', 'methodArn': 'arn:aws:fakearn'}


def generate_jwt_token() -> bytes:
    jwt_headers = {
        "kid": "PVO2XYKpHl8aWm+w0M0xz3CFKi/nJU3tGI2Gs49IAIE=",
        "alg": "RS256"
    }

    jwt_data = {
        "sub": EVENT_SUB,
        "token_use": "access",
        "scope": "hallebarde-dev/api",
        "auth_time": 1582280995,
        "iss": "https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_iSIESzXH1",
        "exp": 1582284595,
        "iat": 1582280995,
        "version": 2,
        "jti": "3bee9e21-3395-4db6-90f3-e363145675cc",
        "client_id": "4dh314ble4s1i8uhleovp3489g"
    }

    jwt_private_key = generate_private_key()
    jwt_token = jwt.encode(jwt_data, jwt_private_key, headers=jwt_headers, algorithm='RS256')
    return jwt_token


def generate_private_key() -> str:
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048)

    # get private key in PEM container format
    pem = key.private_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                            encryption_algorithm=serialization.NoEncryption())

    # decode to printable strings
    private_key_str = pem.decode('utf-8')

    return private_key_str
