import os

from behave import given
from behave.runner import Context
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

client_id = os.environ.get('end2end_client_id')
client_secret = os.environ.get('end2end_client_secret')


@given('I am authenticated to use the Hallebarde file transfer services')
def given_authenticated_on_cognito(context: Context):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(
        token_url='https://dev-filetransfer.auth.eu-west-1.amazoncognito.com/oauth2/token',
        client_id=client_id,
        client_secret=client_secret
    )

    context.authorization_token = token.get('access_token')
